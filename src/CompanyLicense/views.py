from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db.models import Max

from config.settings import LICENSE_ACTIVE

from django.core.exceptions import PermissionDenied

from django.utils import timezone

from .serializers import LicenseSerializer, CompanySerializer

from .models import License, Company
from src.CameraAlgorithms.models import CameraAlgorithm, Camera


class LicenseViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LicenseSerializer(data=request.data)
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


class LicenseInfoView(APIView):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if LICENSE_ACTIVE:
            try:
                company = License.objects.last()
                if company is None and LICENSE_ACTIVE:
                    raise PermissionDenied("No active license")
            except License.DoesNotExist:
                return Response({"error": "Company not found"}, status=404)

            is_license_active = f"{company.valid_until - timezone.now().date()}"

            count_days = int(is_license_active.split(",")[0].split(" ")[0]) + 1
            if count_days < 0:
                count_days = 0
        else:
            company = None
        active_cameras_count = Camera.objects.filter(is_active=True).count()
        active_algorithms_count = (
            CameraAlgorithm.objects.values("algorithm").distinct().count()
        )

        response_data = {
            "date_joined": company.date_joined if company else None,
            "valid_until": company.valid_until if company else None,
            "licence_is_active": company.is_active if company else None,
            "licence_count_cameras": company.count_cameras if company else None,
            "licence_neurons_active": company.neurons_active if company else None,
            "company_active_count_cameras": active_cameras_count,
            "company_active_count_neurons": active_algorithms_count,
            "days_left": f"{count_days} days" if company else None,
        }
        return Response(response_data, status=200)


class CompanyView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = Company.objects.filter(my_company=True)
        max_id = queryset.aggregate(max_id=Max('id'))['max_id']
        queryset = queryset.filter(id=max_id)

        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['my_company'] = True

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            company = License.objects.last()
            if company is None:
                raise PermissionDenied("No active license")

            is_license_active = f"{company.valid_until - timezone.now().date()}"

            count_days = int(is_license_active.split(",")[0].split(" ")[0]) + 1
            if count_days < 0:
                count_days = 0
        except:
            count_days = None

        try:
            company = Company.objects.filter(my_company=True).last()
            name_company = company.name_company
        except:
            name_company = None

        response_data = {
            "count_days": f"{count_days} days",
            "name_company": name_company,
        }

        return Response(response_data)
