from django.urls import path

from src.CompanyLicense.views import CompanyViewSet, CompanyInfoView


urlpatterns = [
    path('create_license/', CompanyViewSet.as_view(), name="create_license"),
    path('info/', CompanyInfoView.as_view(), name='company_info'),

]
