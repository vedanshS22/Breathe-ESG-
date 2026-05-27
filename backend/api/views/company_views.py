from django.db import IntegrityError
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
        name = str(request.data.get("name", "")).strip()
        if not name:
            return failure(
                "Company validation failed.",
                status.HTTP_400_BAD_REQUEST,
                {"name": ["This field is required."]},
            )

        existing_company = Company.objects.filter(name__iexact=name).first()
        if existing_company:
            return success(CompanySerializer(existing_company).data)

        serializer = CompanySerializer(data={**request.data, "name": name})
        if not serializer.is_valid():
            return failure("Company validation failed.", status.HTTP_400_BAD_REQUEST, serializer.errors)
        try:
            company = serializer.save()
        except IntegrityError:
            existing_company = Company.objects.filter(name__iexact=name).first()
            if existing_company:
                return success(CompanySerializer(existing_company).data)
            return failure("Company could not be created.", status.HTTP_400_BAD_REQUEST)
        return success(CompanySerializer(company).data, status.HTTP_201_CREATED)
