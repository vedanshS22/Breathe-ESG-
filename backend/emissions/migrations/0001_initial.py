from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="DataSource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source_type", models.CharField(choices=[("sap", "SAP fuel/procurement flat file"), ("utility", "Utility electricity portal export"), ("travel", "Corporate travel platform export")], max_length=50)),
                ("display_name", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sources", to="emissions.company")),
            ],
            options={"ordering": ["company__name", "source_type"], "unique_together": {("company", "source_type")}},
        ),
        migrations.CreateModel(
            name="RawUpload",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="uploads/%Y/%m/%d/")),
                ("original_filename", models.CharField(max_length=255)),
                ("file_size", models.PositiveIntegerField(default=0)),
                ("content_type", models.CharField(blank=True, max_length=120)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(choices=[("uploaded", "Uploaded"), ("processed", "Processed"), ("partial", "Partial"), ("failed", "Failed")], default="uploaded", max_length=20)),
                ("row_count", models.PositiveIntegerField(default=0)),
                ("successful_count", models.PositiveIntegerField(default=0)),
                ("failed_count", models.PositiveIntegerField(default=0)),
                ("error_message", models.TextField(blank=True)),
                ("source", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="uploads", to="emissions.datasource")),
            ],
            options={"ordering": ["-uploaded_at"]},
        ),
        migrations.CreateModel(
            name="EmissionRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source_type", models.CharField(max_length=50)),
                ("source_row_number", models.PositiveIntegerField(blank=True, null=True)),
                ("source_reference", models.CharField(blank=True, max_length=255)),
                ("scope", models.CharField(max_length=20)),
                ("category", models.CharField(max_length=100)),
                ("quantity", models.FloatField(blank=True, null=True)),
                ("normalized_unit", models.CharField(blank=True, max_length=50)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("raw_data", models.JSONField()),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("is_suspicious", models.BooleanField(default=False)),
                ("suspicious_reason", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("locked", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                ("rejected_at", models.DateTimeField(blank=True, null=True)),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="records", to="emissions.company")),
                ("raw_upload", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="records", to="emissions.rawupload")),
                ("source", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="records", to="emissions.datasource")),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.CreateModel(
            name="IngestionIssue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("stage", models.CharField(choices=[("parsing", "Parsing"), ("normalization", "Normalization"), ("validation", "Validation"), ("persistence", "Persistence")], max_length=40)),
                ("row_number", models.PositiveIntegerField(blank=True, null=True)),
                ("message", models.TextField()),
                ("raw_data", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("raw_upload", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="issues", to="emissions.rawupload")),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=100)),
                ("old_value", models.JSONField(blank=True, null=True)),
                ("new_value", models.JSONField(blank=True, null=True)),
                ("changed_by", models.CharField(max_length=255)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("record", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="audit_logs", to="emissions.emissionrecord")),
            ],
            options={"ordering": ["-timestamp", "-id"]},
        ),
        migrations.AddIndex(
            model_name="emissionrecord",
            index=models.Index(fields=["company", "status"], name="emissions_e_company_883fb6_idx"),
        ),
        migrations.AddIndex(
            model_name="emissionrecord",
            index=models.Index(fields=["company", "is_suspicious"], name="emissions_e_company_6ef689_idx"),
        ),
        migrations.AddIndex(
            model_name="emissionrecord",
            index=models.Index(fields=["source_type"], name="emissions_e_source__e5a952_idx"),
        ),
    ]

