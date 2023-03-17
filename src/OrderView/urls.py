from django.urls import path
from .views import (
    GetAllProductAPIView,
    GetOrderDataByZlecenieAPIView,
)

urlpatterns = [
    path(
        "by-order/<str:zlecenie_id>/",
        GetOrderDataByZlecenieAPIView.as_view(),
        name="get_orders_by_id",
    ),
    path("all-orders/", GetAllProductAPIView.as_view(), name="get_all_orders"),
    path("test/", get_order_test.as_view(), name="test")
]
