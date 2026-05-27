import csv
import json

from django.db.models import Q
from django.http import HttpResponse
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

        page_size = parse_positive_int(request.query_params.get("page_size"), 50, maximum=250)
        page = parse_positive_int(request.query_params.get("page"), 1)
        offset = request.query_params.get("offset")
        limit = request.query_params.get("limit")
        if limit is not None or offset is not None:
            page_size = parse_positive_int(limit, page_size, maximum=250)
            start = parse_positive_int(offset, 0, allow_zero=True)
            page = (start // page_size) + 1
        else:
            start = (page - 1) * page_size
        end = start + page_size
        count = records.count()
        serializer = EmissionRecordSerializer(records[start:end], many=True)
        return success(
            {
                "count": count,
                "page": page,
                "page_size": page_size,
                "limit": page_size,
                "offset": start,
                "next_offset": end if end < count else None,
                "previous_offset": max(start - page_size, 0) if start > 0 else None,
                "total_pages": (count + page_size - 1) // page_size if page_size else 1,
                "results": serializer.data,
            }
        )

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


def parse_positive_int(value, default, maximum=None, allow_zero=False):
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default
    lower_bound = 0 if allow_zero else 1
    number = max(number, lower_bound)
    if maximum:
        number = min(number, maximum)
    return number


def filtered_records(request):
    view = RecordListView()
    records = EmissionRecord.objects.select_related("company", "source", "raw_upload").all()
    return view.apply_filters(records, request)


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


class ExportRawRecordsView(APIView):
    def get(self, request):
        records = filtered_records(request)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="breathe_esg_raw_rows.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "record_id",
                "upload_file",
                "source_type",
                "source_row_number",
                "source_reference",
                "raw_data_json",
            ]
        )
        for record in records.iterator():
            writer.writerow(
                [
                    record.id,
                    record.raw_upload.original_filename,
                    record.source_type,
                    record.source_row_number,
                    record.source_reference,
                    json.dumps(record.raw_data, ensure_ascii=False),
                ]
            )
        return response


class ExportNormalizedRecordsView(APIView):
    def get(self, request):
        records = filtered_records(request)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="breathe_esg_normalized_records.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "record_id",
                "upload_file",
                "source_type",
                "scope",
                "category",
                "quantity",
                "normalized_unit",
                "start_date",
                "end_date",
                "status",
                "locked",
                "is_suspicious",
                "suspicious_reason",
                "source_reference",
            ]
        )
        for record in records.iterator():
            writer.writerow(
                [
                    record.id,
                    record.raw_upload.original_filename,
                    record.source_type,
                    record.scope,
                    record.category,
                    record.quantity,
                    record.normalized_unit,
                    record.start_date,
                    record.end_date,
                    record.status,
                    record.locked,
                    record.is_suspicious,
                    record.suspicious_reason,
                    record.source_reference,
                ]
            )
        return response


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
