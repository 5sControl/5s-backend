from rest_framework.views import APIView
from django.views import View
from django.http import HttpResponse
from .models import Company
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]
