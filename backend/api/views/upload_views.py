from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from api.responses import failure, success
from emissions.models import RawUpload
from emissions.serializers import RawUploadSerializer
from services.exceptions import IngestionError
from services.ingestion.upload_service import UploadService


class UploadListView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        uploads = RawUpload.objects.select_related("source", "source__company").all()[:50]
        return success({"results": RawUploadSerializer(uploads, many=True).data})

    def post(self, request):
        service = UploadService()
        try:
            raw_upload = service.process_upload(
                company_id=request.data.get("company_id"),
                source_type=request.data.get("source_type"),
                uploaded_file=request.FILES.get("file"),
            )
        except IngestionError as exc:
            return failure(str(exc), status.HTTP_400_BAD_REQUEST)

        return success(RawUploadSerializer(raw_upload).data, status.HTTP_201_CREATED)

