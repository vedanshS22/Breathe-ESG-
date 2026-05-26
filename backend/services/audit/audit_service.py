from emissions.models import AuditLog


class AuditService:
    @staticmethod
    def log(record, action, changed_by, old_value=None, new_value=None):
        return AuditLog.objects.create(
            record=record,
            action=action,
            changed_by=changed_by,
            old_value=old_value,
            new_value=new_value,
        )

