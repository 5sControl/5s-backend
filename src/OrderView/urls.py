from django.urls import path
from .views import (
    GetAllProductAPIView,
    GetOrderDataByZlecenieAPIView,
    CreateConectionAPIView,
    GetDatabasesAPIView,
    DeleteConectionAPIView,
    GetProductByIdAPIView,
)

urlpatterns = [
    # get data
    path(
        "by-order/<str:zlecenie_id>/",
        GetOrderDataByZlecenieAPIView.as_view(),
        name="get orders by id",
    ),
    path("all-orders/", GetAllProductAPIView.as_view(), name="get all orders"),
    path("search/", GetProductByIdAPIView.as_view(), name="get order by id"),
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
]
