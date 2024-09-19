from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.DatabaseConnections.views import ActiveResourceView, GetOdooAllItems, ConnectionInfoView


router = DefaultRouter()
router.register(r"connections", ConnectionInfoView, basename="connections")

urlpatterns = [
    path("status/", ActiveResourceView.as_view(), name="connector-status"),
    path("get_odoo_all_items/", GetOdooAllItems.as_view(), name="get_odoo_all_items"),
    path("", include(router.urls)),
]
