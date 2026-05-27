from collections import Counter

from django.db.models import Count
from rest_framework.views import APIView

from api.responses import success
from emissions.models import AuditLog, EmissionRecord, RawUpload
from emissions.serializers import AuditLogSerializer, EmissionRecordSerializer, RawUploadSerializer


class DashboardView(APIView):
    def get(self, request):
        counts = {
            "uploads": RawUpload.objects.count(),
            "records": EmissionRecord.objects.count(),
            "pending": EmissionRecord.objects.filter(status=EmissionRecord.PENDING).count(),
            "approved": EmissionRecord.objects.filter(status=EmissionRecord.APPROVED).count(),
            "rejected": EmissionRecord.objects.filter(status=EmissionRecord.REJECTED).count(),
            "locked": EmissionRecord.objects.filter(locked=True).count(),
            "suspicious": EmissionRecord.objects.filter(is_suspicious=True).count(),
            "failed_uploads": RawUpload.objects.filter(status=RawUpload.FAILED).count(),
        }
        by_source = list(
            EmissionRecord.objects.values("source_type")
            .annotate(count=Count("id"))
            .order_by("source_type")
        )
        recent_uploads = RawUpload.objects.select_related("source", "source__company").all()[:5]
        top_suspicious_categories = list(
            EmissionRecord.objects.filter(is_suspicious=True)
            .values("category")
            .annotate(count=Count("id"))
            .order_by("-count", "category")[:5]
        )
        reason_counter = Counter()
        unit_counter = Counter()
        for reason_text in EmissionRecord.objects.filter(is_suspicious=True).values_list(
            "suspicious_reason", flat=True
        ):
            for reason in [item.strip() for item in reason_text.split(";") if item.strip()]:
                reason_counter[reason] += 1
                if reason.startswith("Unknown unit:"):
                    unit_counter[reason.replace("Unknown unit:", "").strip()] += 1
        top_issue_reasons = [
            {"reason": reason, "count": count}
            for reason, count in reason_counter.most_common(5)
        ]
        top_failed_units = [
            {"unit": unit, "count": count}
            for unit, count in unit_counter.most_common(5)
        ]
        attention_queue = (
            EmissionRecord.objects.select_related("company", "source", "raw_upload")
            .filter(status=EmissionRecord.PENDING)
            .order_by("-is_suspicious", "-created_at")[:8]
        )
        recent_audit = AuditLog.objects.select_related("record").all()[:5]
        return success(
            {
                "counts": counts,
                "by_source": by_source,
                "top_suspicious_categories": top_suspicious_categories,
                "top_issue_reasons": top_issue_reasons,
                "top_failed_units": top_failed_units,
                "recent_uploads": RawUploadSerializer(recent_uploads, many=True).data,
                "attention_queue": EmissionRecordSerializer(attention_queue, many=True).data,
                "recent_audit": AuditLogSerializer(recent_audit, many=True).data,
            }
        )
