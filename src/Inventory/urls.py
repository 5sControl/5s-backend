from django.urls import path, include

from src.Inventory.views import (
    ItemsListAPIView,
    ItemsRetrieveAPIView,
    ItemsHistoryViewSet,
    ItemsCreateAPIView,
    HistoryViewSet,
)


urlpatterns = [
    path("items/", ItemsListAPIView.as_view(), name="items-list"),
    path("items/create/", ItemsCreateAPIView.as_view(), name="items-create"),
    path("items/<int:id>/", ItemsRetrieveAPIView.as_view(), name="items-detail"),
    path(
        "history/<str:date>/<str:start_time>/<str:end_time>/<int:item_id>/",
        ItemsHistoryViewSet.as_view(),
    ),
    path(
        "history/<str:date>/<str:start_time>/<str:end_time>/",
        ItemsHistoryViewSet.as_view(),
    ),
    path("search/<str:date>/<int:item_id>/", HistoryViewSet.as_view(), name="Search date and item_id")
]
