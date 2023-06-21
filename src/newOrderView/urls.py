from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    GetOperation,
    GetOrders,
    GetOrderByDetail,
    GetWhnetOperation,
    GetMachine,
    GetFiltrationsData,
)

router = DefaultRouter()
router.register(r"filtration-data", GetFiltrationsData, basename="filtration-data")

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
    path("", include(router.urls)),
]
