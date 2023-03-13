from django.urls import path
from .views import (
    GetAllDataAPIView,
    GetAllProductAPIView,
    GetOrderApiView,
    GetOrderDataByindexAPIView,
    GetOrderDataByZlecenieAPIView,
)

urlpatterns = [
    path("", GetAllDataAPIView.as_view(), name="get_all_orders_with_data"),
    path(
        "by/<str:index>/",
        GetOrderDataByindexAPIView.as_view(),
        name="get_orders_by_id",
    ),
    path(
        "by-order/<str:zlecenie>/",
        GetOrderDataByZlecenieAPIView.as_view(),
        name="get_orders_by_id",
    ),
    path("all/", GetOrderApiView.as_view(), name="get_orders"),
    path("all-orders/", GetAllProductAPIView.as_view(), name="get_all_orders"),
]
