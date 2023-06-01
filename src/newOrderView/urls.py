from django.urls import path

from .views import (
    GetOperation,
    GetOrders
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
]
