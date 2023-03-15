from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from django.utils import timezone

from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Object created successfully",
                    "object": serializer.data,
                },
                status=201,
            )
        else:
            return Response(
                {"success": False, "message": "Object was not successfully"}, status=404
            )


class CompanyInfoView(APIView):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            company = Company.objects.last()
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)

        is_license_active = f"{company.valid_until - timezone.now().date()}"

        response_data = {
            "name_company": company.name_company,
            "date_joined": company.date_joined,
            "valid_until": company.valid_until,
            "licence_is_active": company.is_active,
            "count_cameras": company.count_cameras,
            "neurons_active": company.neurons_active,
            "days_left": is_license_active.split(",")[0],
        }
        return Response(response_data, status=200)
