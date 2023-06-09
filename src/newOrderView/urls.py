from django.urls import path

from .views import (
    GetOperation,
    GetOrders,
    GetOrderByDetail,
    GetWhnetOperation,
)

urlpatterns = [
    path(
        "operations/",
        GetOperation.as_view(),
        name="get-list-operations",
    ),
    path(
        "orders/",
        GetOrders.as_view(),
        name="get-list-order",
    ),
    path(
        "order-detail/",
        GetOrderByDetail.as_view(),
        name="get-order-detail",
    ),
    path(
        "whnet-operations/",
        GetWhnetOperation.as_view(),
        name="get-whnet-operation",
    )
]
