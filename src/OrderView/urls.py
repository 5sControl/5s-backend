from django.urls import path
from .views import (
    GetAllProductAPIView,
    GetOrderDataByindexAPIView,
    GetOrderDataByZlecenieAPIView,
    GetOrderDataByZlecenieAPIView,
)

urlpatterns = [
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
    path("all-orders/", GetAllProductAPIView.as_view(), name="get_all_orders"),
]
