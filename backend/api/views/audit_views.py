from rest_framework.views import APIView

from api.responses import failure, success
from emissions.models import AuditLog, EmissionRecord, IngestionIssue, RawUpload
from emissions.serializers import AuditLogSerializer, IngestionIssueSerializer


class AuditLogListView(APIView):
    def get(self, request):
        logs = AuditLog.objects.select_related("record").all()[:100]
        return success({"results": AuditLogSerializer(logs, many=True).data})


class IngestionIssueListView(APIView):
    def get(self, request):
        issues = IngestionIssue.objects.select_related("raw_upload").all()[:100]
        return success({"results": IngestionIssueSerializer(issues, many=True).data})


class DeleteAllIngestionDataView(APIView):
    def post(self, request):
        if request.data.get("confirm") not in ("DELETE ALL", True):
            return failure("Delete confirmation is required.", 400)

        upload_files = [upload.file for upload in RawUpload.objects.all() if upload.file]
        counts = {
            "records": EmissionRecord.objects.count(),
            "uploads": RawUpload.objects.count(),
            "audit_logs": AuditLog.objects.count(),
            "ingestion_issues": IngestionIssue.objects.count(),
        }

        AuditLog.objects.all().delete()
        IngestionIssue.objects.all().delete()
        EmissionRecord.objects.all().delete()
        RawUpload.objects.all().delete()

        deleted_files = 0
        for file_field in upload_files:
            try:
                file_field.delete(save=False)
                deleted_files += 1
            except Exception:
                pass

        counts["raw_files"] = deleted_files
        return success(counts)
