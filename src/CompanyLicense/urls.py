from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.CompanyLicense.views import CompanyViewSet, CompanyInfoView

company_report = DefaultRouter()

company_report.register(r"create_license", CompanyViewSet, basename="company")

urlpatterns = [
    path('info/', CompanyInfoView.as_view(), name='company_info'),
    path("", include(company_report.urls)),
]
