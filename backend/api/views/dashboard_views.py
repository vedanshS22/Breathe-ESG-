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
            "suspicious": EmissionRecord.objects.filter(is_suspicious=True).count(),
            "failed_uploads": RawUpload.objects.filter(status=RawUpload.FAILED).count(),
        }
        by_source = list(
            EmissionRecord.objects.values("source_type")
            .annotate(count=Count("id"))
            .order_by("source_type")
        )
        recent_uploads = RawUpload.objects.select_related("source", "source__company").all()[:5]
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
                "recent_uploads": RawUploadSerializer(recent_uploads, many=True).data,
                "attention_queue": EmissionRecordSerializer(attention_queue, many=True).data,
                "recent_audit": AuditLogSerializer(recent_audit, many=True).data,
            }
        )

