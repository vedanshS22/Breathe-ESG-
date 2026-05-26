from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from emissions.models import Company
from services.ingestion.upload_service import UploadService


SAMPLES = [
    ("sap", "sap_fuel_flat_file.csv"),
    ("utility", "utility_portal_export.csv"),
    ("travel", "travel_platform_export.csv"),
]


class Command(BaseCommand):
    help = "Seed a demo company and ingest the bundled sample source files."

    def handle(self, *args, **options):
        company, _created = Company.objects.get_or_create(name="Northstar Manufacturing")
        service = UploadService()
        sample_dir = Path(__file__).resolve().parents[4] / "sample_data"

        for source_type, filename in SAMPLES:
            path = sample_dir / filename
            if not path.exists():
                self.stderr.write(f"Missing sample file: {path}")
                continue

            with path.open("rb") as handle:
                django_file = File(handle, name=filename)
                raw_upload = service.process_upload(
                    company_id=company.id,
                    source_type=source_type,
                    uploaded_file=django_file,
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Ingested {filename}: {raw_upload.successful_count} records, "
                    f"{raw_upload.failed_count} issues"
                )
            )
