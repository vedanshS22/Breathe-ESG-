import logging

from django.db import DatabaseError, IntegrityError
from rest_framework import status
from rest_framework.views import APIView

from api.responses import failure, success
from emissions.models import Company
from emissions.serializers import CompanySerializer

logger = logging.getLogger(__name__)


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

        try:
            existing_company = Company.objects.filter(name__iexact=name).first()
            if existing_company:
                return success(CompanySerializer(existing_company).data)

            serializer = CompanySerializer(data={**request.data, "name": name})
            if not serializer.is_valid():
                return failure("Company validation failed.", status.HTTP_400_BAD_REQUEST, serializer.errors)
            company = serializer.save()
        except IntegrityError:
            existing_company = Company.objects.filter(name__iexact=name).first()
            if existing_company:
                return success(CompanySerializer(existing_company).data)
            return failure("Company could not be created.", status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            logger.exception("Database error while creating company")
            return failure(
                "Company could not be created because the deployed database is not ready. Run migrations and try again.",
                status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            logger.exception("Unexpected error while creating company")
            return failure("Company could not be created.", status.HTTP_400_BAD_REQUEST)
        return success(CompanySerializer(company).data, status.HTTP_201_CREATED)
