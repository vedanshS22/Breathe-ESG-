from rest_framework import serializers

from emissions.models import (
    AuditLog,
    Company,
    DataSource,
    EmissionRecord,
    IngestionIssue,
    RawUpload,
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "created_at"]


class DataSourceSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = DataSource
        fields = ["id", "company", "company_name", "source_type", "display_name", "created_at"]


class RawUploadSerializer(serializers.ModelSerializer):
    source_type = serializers.CharField(source="source.source_type", read_only=True)
    company_id = serializers.IntegerField(source="source.company_id", read_only=True)

    class Meta:
        model = RawUpload
        fields = [
            "id",
            "source",
            "source_type",
            "company_id",
            "file",
            "original_filename",
            "file_size",
            "content_type",
            "uploaded_at",
            "status",
            "row_count",
            "successful_count",
            "failed_count",
            "error_message",
        ]


class EmissionRecordSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    upload_filename = serializers.CharField(source="raw_upload.original_filename", read_only=True)

    class Meta:
        model = EmissionRecord
        fields = [
            "id",
            "company",
            "company_name",
            "source",
            "raw_upload",
            "upload_filename",
            "source_type",
            "source_row_number",
            "source_reference",
            "scope",
            "category",
            "quantity",
            "normalized_unit",
            "start_date",
            "end_date",
            "raw_data",
            "metadata",
            "is_suspicious",
            "suspicious_reason",
            "status",
            "locked",
            "created_at",
            "updated_at",
            "approved_at",
            "rejected_at",
        ]
        read_only_fields = [
            "status",
            "locked",
            "created_at",
            "updated_at",
            "approved_at",
            "rejected_at",
        ]


class IngestionIssueSerializer(serializers.ModelSerializer):
    upload_filename = serializers.CharField(source="raw_upload.original_filename", read_only=True)

    class Meta:
        model = IngestionIssue
        fields = [
            "id",
            "raw_upload",
            "upload_filename",
            "stage",
            "row_number",
            "message",
            "raw_data",
            "created_at",
        ]


class AuditLogSerializer(serializers.ModelSerializer):
    record_source_type = serializers.CharField(source="record.source_type", read_only=True)
    record_category = serializers.CharField(source="record.category", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "record",
            "record_source_type",
            "record_category",
            "action",
            "old_value",
            "new_value",
            "changed_by",
            "timestamp",
        ]

