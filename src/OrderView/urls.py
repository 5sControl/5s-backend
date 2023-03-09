from django.urls import path
from .views import GetAllDataAPIView, GetAllOrdersAPIView, GetOrderDataByIdAPIView

urlpatterns = [
    path("", GetAllDataAPIView.as_view(), name="get_all_orders_with_data"),
    path('<str:zlecenie_id>/', GetOrderDataByIdAPIView.as_view(), name='get_orders_by_id'),
    path("all-orders/", GetAllOrdersAPIView.as_view(), name="get_all_orders"),
]
