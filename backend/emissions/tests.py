from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from emissions.models import Company, EmissionRecord, IngestionIssue, RawUpload
from services.ingestion.upload_service import UploadService


class IngestionWorkflowTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Manufacturing")

    def test_sap_upload_preserves_raw_file_and_flags_suspicious_rows(self):
        csv_bytes = (
            "Werk,Buchungsdatum,Material Document,Kraftstoff,Menge,Einheit\n"
            "PLT-01,2026-05-01,4900001,Diesel,5000,L\n"
            "PLT-01,32/13/2026,4900002,Diesel,-25,ltr\n"
        ).encode("utf-8")
        uploaded_file = SimpleUploadedFile(
            "sap_test.csv",
            csv_bytes,
            content_type="text/csv",
        )

        raw_upload = UploadService().process_upload(
            company_id=self.company.id,
            source_type="sap",
            uploaded_file=uploaded_file,
        )

        self.assertEqual(raw_upload.status, RawUpload.PROCESSED)
        self.assertEqual(raw_upload.records.count(), 2)
        self.assertEqual(raw_upload.records.filter(is_suspicious=True).count(), 1)
        self.assertTrue(raw_upload.file.name)

    def test_approval_locks_record_and_rejecting_locked_record_conflicts(self):
        raw_upload = self._ingest_one_record()
        record = raw_upload.records.first()
        client = APIClient()

        approve = client.post(
            f"/api/records/{record.id}/approve/",
            {"actor": "tester@local"},
            format="json",
            HTTP_HOST="localhost",
        )
        self.assertEqual(approve.status_code, 200)

        record.refresh_from_db()
        self.assertEqual(record.status, EmissionRecord.APPROVED)
        self.assertTrue(record.locked)
        self.assertEqual(record.audit_logs.count(), 1)

        reject = client.post(
            f"/api/records/{record.id}/reject/",
            {"actor": "tester@local"},
            format="json",
            HTTP_HOST="localhost",
        )
        self.assertEqual(reject.status_code, 409)

    def test_delete_all_ingestion_data_clears_uploads_records_and_audit(self):
        raw_upload = self._ingest_one_record()
        record = raw_upload.records.first()
        client = APIClient()
        client.post(
            f"/api/records/{record.id}/approve/",
            {"actor": "tester@local"},
            format="json",
            HTTP_HOST="localhost",
        )

        response = client.post(
            "/api/delete-all-ingestion-data/",
            {"confirm": True},
            format="json",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(EmissionRecord.objects.count(), 0)
        self.assertEqual(RawUpload.objects.count(), 0)

    def test_existing_company_create_returns_existing_company(self):
        client = APIClient()

        response = client.post(
            "/api/companies/",
            {"name": " Test Manufacturing "},
            format="json",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Company.objects.filter(name="Test Manufacturing").count(), 1)
        self.assertEqual(response.json()["data"]["id"], self.company.id)

    def test_missing_required_column_persists_failed_upload_issue(self):
        uploaded_file = SimpleUploadedFile(
            "bad_sap.csv",
            (
                "Werk,Buchungsdatum,Material Document,Kraftstoff,Einheit\n"
                "PLT-01,2026-05-01,4900001,Diesel,L\n"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        client = APIClient()

        response = client.post(
            "/api/uploads/",
            {"company_id": self.company.id, "source_type": "sap", "file": uploaded_file},
            format="multipart",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(RawUpload.objects.count(), 1)
        self.assertEqual(RawUpload.objects.first().status, RawUpload.FAILED)
        self.assertEqual(IngestionIssue.objects.count(), 1)

    def test_ingestion_issues_endpoint_includes_validation_warnings(self):
        raw_upload = self._ingest_one_record(
            quantity="-25",
            date_value="32/13/2026",
        )
        record = raw_upload.records.first()
        self.assertTrue(record.is_suspicious)
        client = APIClient()

        response = client.get("/api/ingestion-issues/", HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        results = response.json()["data"]["results"]
        self.assertEqual(results[0]["stage"], "validation")
        self.assertIn("Negative quantity", results[0]["message"])

    def test_therm_is_valid_unit_not_suspicious(self):
        raw_upload = self._ingest_one_record(quantity="24500", unit="therm")
        record = raw_upload.records.first()

        self.assertEqual(record.normalized_unit, "therm")
        self.assertFalse(record.is_suspicious)
        self.assertEqual(record.suspicious_reason, "")

    def test_raw_and_normalized_exports_are_downloadable(self):
        self._ingest_one_record()
        client = APIClient()

        raw_response = client.get("/api/records/export/raw/", HTTP_HOST="localhost")
        normalized_response = client.get("/api/records/export/normalized/", HTTP_HOST="localhost")

        self.assertEqual(raw_response.status_code, 200)
        self.assertEqual(normalized_response.status_code, 200)
        self.assertIn("raw_data_json", raw_response.content.decode("utf-8"))
        self.assertIn("normalized_unit", normalized_response.content.decode("utf-8"))

    def _ingest_one_record(self, quantity="5000", date_value="2026-05-01", unit="L"):
        uploaded_file = SimpleUploadedFile(
            "sap_test.csv",
            (
                "Werk,Buchungsdatum,Material Document,Kraftstoff,Menge,Einheit\n"
                f"PLT-01,{date_value},4900001,Diesel,{quantity},{unit}\n"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        return UploadService().process_upload(
            company_id=self.company.id,
            source_type="sap",
            uploaded_file=uploaded_file,
        )
