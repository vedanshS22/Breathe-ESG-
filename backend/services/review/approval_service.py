from django.db import transaction
from django.utils import timezone

from emissions.models import EmissionRecord
from services.audit.audit_service import AuditService
from services.exceptions import WorkflowConflict


class ReviewService:
    def approve(self, record_id, actor):
        with transaction.atomic():
            record = EmissionRecord.objects.select_for_update().get(pk=record_id)
            if record.locked:
                raise WorkflowConflict("Approved records are locked for audit.")
            if record.status == EmissionRecord.APPROVED:
                raise WorkflowConflict("Record is already approved.")

            old_value = {"status": record.status, "locked": record.locked}
            record.status = EmissionRecord.APPROVED
            record.locked = True
            record.approved_at = timezone.now()
            record.rejected_at = None
            record.save(update_fields=["status", "locked", "approved_at", "rejected_at", "updated_at"])
            AuditService.log(
                record=record,
                action="approved",
                changed_by=actor,
                old_value=old_value,
                new_value={"status": record.status, "locked": record.locked},
            )
            return record

    def reject(self, record_id, actor, reason=""):
        with transaction.atomic():
            record = EmissionRecord.objects.select_for_update().get(pk=record_id)
            if record.locked:
                raise WorkflowConflict("Locked records cannot be rejected.")
            if record.status == EmissionRecord.REJECTED:
                raise WorkflowConflict("Record is already rejected.")

            old_value = {"status": record.status, "locked": record.locked}
            record.status = EmissionRecord.REJECTED
            record.rejected_at = timezone.now()
            record.save(update_fields=["status", "rejected_at", "updated_at"])
            AuditService.log(
                record=record,
                action="rejected",
                changed_by=actor,
                old_value=old_value,
                new_value={"status": record.status, "reason": reason},
            )
            return record

