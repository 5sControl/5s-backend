from django.urls import path

from .views import GetAllDataAPIView, GetAllOrdersAPIView, GetOrderDataByIdAPIView, TestApiView

urlpatterns = [
    path("", GetAllDataAPIView.as_view(), name="get_all_orders_with_data"),
    path('by/<str:zlecenie_id>/', GetOrderDataByIdAPIView.as_view(), name='get_orders_by_id'),
    path("all-orders/", GetAllOrdersAPIView.as_view(), name="get_all_orders"),
    # test
    path("test/", TestApiView.as_view(), name="testapi")
]
