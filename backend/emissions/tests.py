from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from emissions.models import Company, EmissionRecord, RawUpload
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

    def _ingest_one_record(self):
        uploaded_file = SimpleUploadedFile(
            "sap_test.csv",
            (
                "Werk,Buchungsdatum,Material Document,Kraftstoff,Menge,Einheit\n"
                "PLT-01,2026-05-01,4900001,Diesel,5000,L\n"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        return UploadService().process_upload(
            company_id=self.company.id,
            source_type="sap",
            uploaded_file=uploaded_file,
        )
