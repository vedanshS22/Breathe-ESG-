from django.core.exceptions import ValidationError
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DataSource(models.Model):
    SAP = "sap"
    UTILITY = "utility"
    TRAVEL = "travel"

    SOURCE_TYPES = [
        (SAP, "SAP fuel/procurement flat file"),
        (UTILITY, "Utility electricity portal export"),
        (TRAVEL, "Corporate travel platform export"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sources")
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES)
    display_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["company__name", "source_type"]
        unique_together = [("company", "source_type")]

    def __str__(self):
        return self.display_name or self.get_source_type_display()


class RawUpload(models.Model):
    UPLOADED = "uploaded"
    PROCESSED = "processed"
    PARTIAL = "partial"
    FAILED = "failed"

    STATUS_CHOICES = [
        (UPLOADED, "Uploaded"),
        (PROCESSED, "Processed"),
        (PARTIAL, "Partial"),
        (FAILED, "Failed"),
    ]

    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="uploads")
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(default=0)
    content_type = models.CharField(max_length=120, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=UPLOADED)
    row_count = models.PositiveIntegerField(default=0)
    successful_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    @property
    def company(self):
        return self.source.company

    def __str__(self):
        return f"{self.original_filename} ({self.status})"


class EmissionRecord(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="records")
    source = models.ForeignKey(DataSource, on_delete=models.PROTECT, related_name="records")
    raw_upload = models.ForeignKey(
        RawUpload,
        on_delete=models.PROTECT,
        related_name="records",
    )
    source_type = models.CharField(max_length=50)
    source_row_number = models.PositiveIntegerField(null=True, blank=True)
    source_reference = models.CharField(max_length=255, blank=True)

    scope = models.CharField(max_length=20)
    category = models.CharField(max_length=100)
    quantity = models.FloatField(null=True, blank=True)
    normalized_unit = models.CharField(max_length=50, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    raw_data = models.JSONField()
    metadata = models.JSONField(default=dict, blank=True)

    is_suspicious = models.BooleanField(default=False)
    suspicious_reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["company", "status"], name="emissions_e_company_883fb6_idx"),
            models.Index(fields=["company", "is_suspicious"], name="emissions_e_company_6ef689_idx"),
            models.Index(fields=["source_type"], name="emissions_e_source__e5a952_idx"),
        ]

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    def __str__(self):
        return f"{self.source_type}:{self.scope}:{self.category}:{self.quantity}"


class IngestionIssue(models.Model):
    PARSING = "parsing"
    NORMALIZATION = "normalization"
    VALIDATION = "validation"
    PERSISTENCE = "persistence"

    STAGE_CHOICES = [
        (PARSING, "Parsing"),
        (NORMALIZATION, "Normalization"),
        (VALIDATION, "Validation"),
        (PERSISTENCE, "Persistence"),
    ]

    raw_upload = models.ForeignKey(RawUpload, on_delete=models.CASCADE, related_name="issues")
    stage = models.CharField(max_length=40, choices=STAGE_CHOICES)
    row_number = models.PositiveIntegerField(null=True, blank=True)
    message = models.TextField()
    raw_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.stage}: row {self.row_number or '-'}"


class AuditLog(models.Model):
    record = models.ForeignKey(EmissionRecord, on_delete=models.CASCADE, related_name="audit_logs")
    action = models.CharField(max_length=100)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    changed_by = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp", "-id"]

    def __str__(self):
        return f"{self.action} record={self.record_id}"
