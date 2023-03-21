from rest_framework.routers import DefaultRouter
from django.urls import path, include
from src.Inventory.views import ItemsViewSet


router_inventory = DefaultRouter()

router_inventory.register(r"items", ItemsViewSet, basename="items")

urlpatterns = [
    path("", include(router_inventory.urls)),
]
