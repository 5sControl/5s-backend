from django.urls import path

from .views import (
    GetOperation,
    GetOrders,
    GetOrderByDetail,
    GetWhnetOperation,
    GetMachine,
    FiltrationsDataView,
    GetOperationsDuration,
    GetOrderPackaging
)


urlpatterns = [
    path(
        "operations/",
        GetOperation.as_view(),
        name="get-list-operations",
    ),
    path(
        "machine/",
        GetMachine.as_view(),
        name="get-list-machine",
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
    ),
    path(
        "filtration-data",
        FiltrationsDataView.as_view(),
        name="filtrations-data",
    ),
    path(
        "avg-operations-duration",
        GetOperationsDuration.as_view(),
        name="avg-duration",
    ),
    path(
        "order-packaging/",
        GetOrderPackaging.as_view(),
        name="order-packaging",
    )
]
