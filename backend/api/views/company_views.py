from rest_framework import status
from rest_framework.views import APIView

from api.responses import failure, success
from emissions.models import Company
from emissions.serializers import CompanySerializer


class CompanyListView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        return success({"results": CompanySerializer(companies, many=True).data})

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if not serializer.is_valid():
            return failure("Company validation failed.", status.HTTP_400_BAD_REQUEST, serializer.errors)
        company = serializer.save()
        return success(CompanySerializer(company).data, status.HTTP_201_CREATED)

