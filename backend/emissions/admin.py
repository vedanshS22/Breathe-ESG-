from django.contrib import admin

from emissions.models import (
    AuditLog,
    Company,
    DataSource,
    EmissionRecord,
    IngestionIssue,
    RawUpload,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ("company", "source_type", "display_name", "created_at")
    list_filter = ("source_type",)
    search_fields = ("company__name", "display_name")


@admin.register(RawUpload)
class RawUploadAdmin(admin.ModelAdmin):
    list_display = (
        "original_filename",
        "source",
        "status",
        "row_count",
        "successful_count",
        "failed_count",
        "uploaded_at",
    )
    list_filter = ("status", "source__source_type")
    search_fields = ("original_filename",)


@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company",
        "source_type",
        "scope",
        "category",
        "quantity",
        "normalized_unit",
        "is_suspicious",
        "status",
        "locked",
    )
    list_filter = ("source_type", "scope", "status", "is_suspicious", "locked")
    search_fields = ("source_reference", "category", "raw_data")


@admin.register(IngestionIssue)
class IngestionIssueAdmin(admin.ModelAdmin):
    list_display = ("raw_upload", "stage", "row_number", "message", "created_at")
    list_filter = ("stage",)
    search_fields = ("message",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("record", "action", "changed_by", "timestamp")
    list_filter = ("action",)
    search_fields = ("changed_by", "action")

