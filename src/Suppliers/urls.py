from django.urls import path
from rest_framework.routers import DefaultRouter

from src.Suppliers.views import SuppliersView, CountryListView

router = DefaultRouter()
router.register(r"company", SuppliersView, basename="company_info")

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
]

urlpatterns += router.urls
