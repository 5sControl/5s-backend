from django.urls import path
from .views import (
    GetAllProductAPIView,
    GetOrderDataByZlecenieAPIView,
    OperationNameApiView,
    CreateConectionAPIView,
    GetDatabasesAPIView,
    DeleteConectionAPIView,
    IndexOperationsView,
    IndexOperationDetailView,
)

urlpatterns = [
    # get data
    path(
        "by-order/<str:zlecenie_id>/",
        GetOrderDataByZlecenieAPIView.as_view(),
        name="get orders by id",
    ),
    path("all-orders/", GetAllProductAPIView.as_view(), name="get all orders"),
    path("get-operations/", OperationNameApiView.as_view(), name="get operations name"),
    # database configuration
    path(
        "create-connection/", CreateConectionAPIView.as_view(), name="mssql connection"
    ),
    path(
        "get-connections/",
        GetDatabasesAPIView.as_view(),
        name="get list of all database connections",
    ),
    path(
        "delete-connection/<int:id>/",
        DeleteConectionAPIView.as_view(),
        name="delete connection from connection database",
    ),
    path('index_operations/', IndexOperationsView.as_view(), name='index_operations'),
    path('index_operations/<int:pk>/', IndexOperationDetailView.as_view(), name='index_operations_detail'),
]
