from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.CompanyLicense.views import CompanyViewSet

company_report = DefaultRouter()

company_report.register(r"create_license", CompanyViewSet, basename="company")

urlpatterns = [
    # path('create_licenses/', LicenseView.as_view(), name='create licenses'),
    path("", include(company_report.urls)),
]
