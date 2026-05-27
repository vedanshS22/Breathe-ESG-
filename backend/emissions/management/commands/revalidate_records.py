from django.core.management.base import BaseCommand

from emissions.models import EmissionRecord
from validators.validation_engine import evaluate_record


class Command(BaseCommand):
    help = "Re-evaluate suspicious flags for existing normalized records."

    def handle(self, *args, **options):
        updated = 0
        for record in EmissionRecord.objects.all().iterator():
            metadata = record.metadata or {}
            warnings = metadata.get("normalization_warnings", [])
            cleaned_warnings = [
                warning
                for warning in warnings
                if warning.strip().lower() not in {"unknown unit: therm", "unknown unit: therms"}
            ]
            metadata["normalization_warnings"] = cleaned_warnings

            payload = {
                "source_type": record.source_type,
                "category": record.category,
                "quantity": record.quantity,
                "normalized_unit": record.normalized_unit,
                "start_date": record.start_date,
                "end_date": record.end_date,
                "metadata": metadata,
            }
            validation = evaluate_record(payload)
            record.metadata = metadata
            record.is_suspicious = validation["is_suspicious"]
            record.suspicious_reason = validation["suspicious_reason"]
            record.save(update_fields=["metadata", "is_suspicious", "suspicious_reason", "updated_at"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Revalidated {updated} records."))

