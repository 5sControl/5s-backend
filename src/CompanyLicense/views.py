from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from src.Core.const import SERVER_URL

from django.core.exceptions import PermissionDenied

from django.utils import timezone

from .serializers import CompanySerializer

from .models import Company
from src.CameraAlgorithms.models import CameraAlgorithm, Camera
import requests


class CompanyViewSet(APIView):
    permission_classes = [IsAuthenticated]

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
            if company is None:
                raise PermissionDenied("No active license")
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)

        is_license_active = f"{company.valid_until - timezone.now().date()}"

        count_days = int(is_license_active.split(",")[0].split(" ")[0])
        if count_days < 0:
            count_days = 0

        active_cameras_count = Camera.objects.filter(is_active=True).count()
        active_algorithms_count = (
            CameraAlgorithm.objects.values("algorithm").distinct().count()
        )

        response_data = {
            "name_company": company.name_company,
            "date_joined": company.date_joined,
            "valid_until": company.valid_until,
            "licence_is_active": company.is_active,
            "licence_count_cameras": company.count_cameras,
            "licence_neurons_active": company.neurons_active,
            "company_active_count_cameras": active_cameras_count,
            "company_active_count_neurons": active_algorithms_count,
            "days_left": f"{count_days} days",
        }
        return Response(response_data, status=200)


@api_view(['GET'])
def version(request):
    versions = []
    versions = versions + [{
        "name": "5S Control version",
        "version": "v0.3.8",
        "date": "05.31.2023",
        "description": ""
    }]

    try:
        js_algs_port = 3333
        request = requests.post(
            url=f"{SERVER_URL}:{js_algs_port}/info"
        )
        request_json = request.json()
        versions = versions + request_json
    except Exception as e:
        return Response({"error": f"Versions not found: {e}"}, status=404)

    return Response(versions)
