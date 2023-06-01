from django.urls import path

from rest_framework.routers import DefaultRouter

from src.CompanyLicense.views import LicenseViewSet, LicenseInfoView, version, CompanyView

router = DefaultRouter()
router.register(r"company", CompanyView, basename="company_info")

urlpatterns = [
    path("create_license/", LicenseViewSet.as_view(), name="create_license"),
    path("info/", LicenseInfoView.as_view(), name="license_info"),
    path('version/', version, name='read-file'),
]

urlpatterns += router.urls
