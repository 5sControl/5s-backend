from rest_framework.views import APIView
from django.utils import timezone

from .models import Company
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]


class CompanyInfoView(APIView):

    def get(self, request):
        try:
            company = Company.objects.last()
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)

        is_license_active = f"{company.valid_until - timezone.now().date()}"

        response_data = {
            'name_company': company.name_company,
            'date_joined': company.date_joined,
            'licence_is_active': company.is_active,
            'count_cameras': company.count_cameras,
            'neurons_active': company.neurons_active,
            'days_left': is_license_active,
        }
        return Response(response_data, status=200)
