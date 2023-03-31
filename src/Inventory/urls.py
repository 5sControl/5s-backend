from rest_framework.routers import DefaultRouter

from django.urls import path, include

from src.Inventory.views import ItemsViewSet, ItemsHistoryViewSet

router_inventory = DefaultRouter()

router_inventory.register(r"items", ItemsViewSet, basename="items")

urlpatterns = [
    path("history/<str:camera_ip>/<str:date>/<str:start_time>/<str:end_time>/<int:item_id>/",
         ItemsHistoryViewSet.as_view()),
    path("history/<str:camera_ip>/<str:date>/<str:start_time>/<str:end_time>/", ItemsHistoryViewSet.as_view()),
    path("", include(router_inventory.urls)),
]
