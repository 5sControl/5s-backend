from django.urls import path
from rest_framework.routers import DefaultRouter

from src.Suppliers.views import SuppliersView

router = DefaultRouter()
router.register(r"company", SuppliersView, basename="company_info")

urlpatterns = [
]

urlpatterns += router.urls
