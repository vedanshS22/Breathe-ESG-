from django.conf import settings
from django.db import transaction

from emissions.models import Company, DataSource, EmissionRecord, IngestionIssue, RawUpload
from services.exceptions import IngestionError, ParserError
from services.categorization.ai_categorizer import AICategorizer
from services.normalizers.registry import get_normalizer
from services.parsers.registry import get_parser
from validators.validation_engine import evaluate_record


SOURCE_DISPLAY_NAMES = {
    "sap": "SAP fuel/procurement flat file",
    "utility": "Utility electricity portal export",
    "travel": "Corporate travel platform export",
}


class UploadService:
    def process_upload(self, *, company_id, source_type, uploaded_file, categorization_mode="manual"):
        categorization_mode = categorization_mode or "manual"
        if categorization_mode not in {"manual", "auto"}:
            raise IngestionError("Unsupported categorization mode.")
        if categorization_mode == "manual" and source_type not in SOURCE_DISPLAY_NAMES:
            raise IngestionError("Unsupported source type.")
        if not uploaded_file:
            raise IngestionError("File is required.")

        file_size = getattr(uploaded_file, "size", 0) or 0
        if file_size == 0:
            raise IngestionError("Uploaded file is empty.")
        if file_size > settings.MAX_UPLOAD_SIZE_BYTES:
            raise IngestionError("Uploaded file exceeds the configured size limit.")

        company = self._get_company(company_id)
        categorizer = AICategorizer()
        source_decision = None
        if categorization_mode == "auto":
            source_decision = categorizer.infer_source_type(uploaded_file)
            source_type = source_decision["source_type"]
        if source_type not in SOURCE_DISPLAY_NAMES:
            raise IngestionError("Unsupported source type.")

        parser = get_parser(source_type, uploaded_file.name)
        normalizer = get_normalizer(source_type)

        with transaction.atomic():
            source, _created = DataSource.objects.get_or_create(
                company=company,
                source_type=source_type,
                defaults={"display_name": SOURCE_DISPLAY_NAMES[source_type]},
            )
            raw_upload = RawUpload.objects.create(
                source=source,
                file=uploaded_file,
                original_filename=uploaded_file.name,
                file_size=file_size,
                content_type=getattr(uploaded_file, "content_type", "") or "",
            )

        try:
            rows = parser.parse(raw_upload.file)
        except ParserError as exc:
            raw_upload.status = RawUpload.FAILED
            raw_upload.error_message = str(exc)
            raw_upload.save(update_fields=["status", "error_message"])
            IngestionIssue.objects.create(
                raw_upload=raw_upload,
                stage=IngestionIssue.PARSING,
                message=str(exc),
            )
            raise IngestionError(str(exc)) from exc

        if not rows:
            raw_upload.status = RawUpload.FAILED
            raw_upload.error_message = "No operational rows found."
            raw_upload.save(update_fields=["status", "error_message"])
            IngestionIssue.objects.create(
                raw_upload=raw_upload,
                stage=IngestionIssue.PARSING,
                message="No operational rows found.",
            )
            raise IngestionError("No operational rows found.")

        with transaction.atomic():
            success_count = 0
            failed_count = 0

            for parsed_row in rows:
                row = parsed_row.data
                parse_error = row.get("__parse_error__")
                if parse_error:
                    failed_count += 1
                    IngestionIssue.objects.create(
                        raw_upload=raw_upload,
                        stage=IngestionIssue.PARSING,
                        row_number=parsed_row.row_number,
                        message=parse_error,
                        raw_data=row,
                    )
                    continue

                try:
                    normalized = normalizer.normalize(row)
                    normalized = categorizer.categorize_record(
                        normalized,
                        source_decision,
                        categorization_mode,
                    )
                    validation = evaluate_record(normalized)
                    EmissionRecord.objects.create(
                        company=company,
                        source=source,
                        raw_upload=raw_upload,
                        source_row_number=parsed_row.row_number,
                        is_suspicious=validation["is_suspicious"],
                        suspicious_reason=validation["suspicious_reason"],
                        **normalized,
                    )
                    success_count += 1
                except Exception as exc:
                    failed_count += 1
                    IngestionIssue.objects.create(
                        raw_upload=raw_upload,
                        stage=IngestionIssue.NORMALIZATION,
                        row_number=parsed_row.row_number,
                        message=str(exc),
                        raw_data=row,
                    )

            raw_upload.row_count = len(rows)
            raw_upload.successful_count = success_count
            raw_upload.failed_count = failed_count
            if success_count and failed_count:
                raw_upload.status = RawUpload.PARTIAL
            elif success_count:
                raw_upload.status = RawUpload.PROCESSED
            else:
                raw_upload.status = RawUpload.FAILED
                raw_upload.error_message = "All rows failed during ingestion."
            raw_upload.save(
                update_fields=[
                    "row_count",
                    "successful_count",
                    "failed_count",
                    "status",
                    "error_message",
                ]
            )
            return raw_upload

    def _get_company(self, company_id):
        if not company_id:
            raise IngestionError("company_id is required.")
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist as exc:
            raise IngestionError("Company does not exist.") from exc
