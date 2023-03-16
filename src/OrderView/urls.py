from django.urls import path
from .views import (
    GetAllProductAPIView,
    GetOrderDataByindexAPIView,
    GetOrderDataByZlecenieAPIView,
    GetOrderDataByZlecenieAPIView,
    TestAPIView,
)

urlpatterns = [
    path(
        "by/<str:index>/",
        GetOrderDataByindexAPIView.as_view(),
        name="get_orders_by_id",
    ),
    path(
        "by-order/<str:zlecenie_id>/",
        GetOrderDataByZlecenieAPIView.as_view(),
        name="get_orders_by_id",
    ),
    path("all-orders/", GetAllProductAPIView.as_view(), name="get_all_orders"),
    # test
    path("test/", TestAPIView.as_view(), name="test"),
]
