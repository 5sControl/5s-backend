from django.urls import path
from .views import (
    GetAllProductAPIView,
    GetOrderDataByZlecenieAPIView,
    TESTGetOrderDataByZlecenieAPIView,
)

urlpatterns = [
    path(
        "by-order/<str:zlecenie_id>/",
        GetOrderDataByZlecenieAPIView.as_view(),
        name="get_orders_by_id",
    ),
    path("all-orders/", GetAllProductAPIView.as_view(), name="get_all_orders"),
    path("test/<str:zlecenie_id>/", TESTGetOrderDataByZlecenieAPIView.as_view(), name="test"),
]
