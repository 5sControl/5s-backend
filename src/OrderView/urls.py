from django.urls import path
from .views import (
    GetAllDataAPIView,
    GetAllOrdersAPIView,
    GetOrderApiView,
    GetOrderDataByIdAPIView,
)

urlpatterns = [
    path("", GetAllDataAPIView.as_view(), name="get_all_orders_with_data"),
    path(
        "by/<str:zlecenie_id>/",
        GetOrderDataByIdAPIView.as_view(),
        name="get_orders_by_id",
    ),
    path("all/", GetOrderApiView.as_view(), name="get_orders"),
    path("all-orders/", GetAllOrdersAPIView.as_view(), name="get_all_orders"),
]
