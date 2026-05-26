from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from api.responses import failure, success
from emissions.models import EmissionRecord
from emissions.serializers import EmissionRecordSerializer
from services.exceptions import WorkflowConflict
from services.review.approval_service import ReviewService


def actor_from_request(request):
    return request.data.get("actor") or request.headers.get("X-Analyst") or "analyst@breathe.local"


class RecordListView(APIView):
    def get(self, request):
        records = EmissionRecord.objects.select_related("company", "source", "raw_upload").all()
        records = self.apply_filters(records, request)

        page_size = min(int(request.query_params.get("page_size", 50)), 100)
        page = max(int(request.query_params.get("page", 1)), 1)
        start = (page - 1) * page_size
        end = start + page_size
        count = records.count()
        serializer = EmissionRecordSerializer(records[start:end], many=True)
        return success({"count": count, "page": page, "page_size": page_size, "results": serializer.data})

    def apply_filters(self, records, request):
        source_type = request.query_params.get("source_type")
        scope = request.query_params.get("scope")
        status_value = request.query_params.get("status")
        suspicious = request.query_params.get("suspicious")
        search = request.query_params.get("search")

        if source_type:
            records = records.filter(source_type=source_type)
        if scope:
            records = records.filter(scope=scope)
        if status_value:
            records = records.filter(status=status_value)
        if suspicious in {"true", "false"}:
            records = records.filter(is_suspicious=suspicious == "true")
        if search:
            records = records.filter(
                Q(category__icontains=search)
                | Q(source_reference__icontains=search)
                | Q(suspicious_reason__icontains=search)
            )
        return records


class SuspiciousRecordListView(APIView):
    def get(self, request):
        records = EmissionRecord.objects.select_related("company", "source", "raw_upload").filter(
            is_suspicious=True
        )
        return success({"results": EmissionRecordSerializer(records[:100], many=True).data})


class RecordDetailView(APIView):
    def get(self, request, record_id):
        record = get_object_or_404(EmissionRecord, pk=record_id)
        return success(EmissionRecordSerializer(record).data)


class ApproveRecordView(APIView):
    def post(self, request, record_id):
        service = ReviewService()
        try:
            record = service.approve(record_id, actor_from_request(request))
        except EmissionRecord.DoesNotExist:
            return failure("Record not found.", status.HTTP_404_NOT_FOUND)
        except WorkflowConflict as exc:
            return failure(str(exc), status.HTTP_409_CONFLICT)
        return success({"status": record.status, "locked": record.locked})


class RejectRecordView(APIView):
    def post(self, request, record_id):
        service = ReviewService()
        try:
            record = service.reject(
                record_id,
                actor_from_request(request),
                reason=request.data.get("reason", ""),
            )
        except EmissionRecord.DoesNotExist:
            return failure("Record not found.", status.HTTP_404_NOT_FOUND)
        except WorkflowConflict as exc:
            return failure(str(exc), status.HTTP_409_CONFLICT)
        return success({"status": record.status, "locked": record.locked})

