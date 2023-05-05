from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    GetAllProductAPIView,
    GetOrderDataByZlecenieAPIView,
    OperationNameApiView,
    CreateDatabaseConnectionAPIView,
    GetDatabasesAPIView,
    DeleteConectionAPIView,
    IndexOperationsView,
)

router = DefaultRouter()
router.register(r"index_stanowisko", IndexOperationsView, basename="index_stanowisko")

urlpatterns = [
    path(
        "by-order/<str:zlecenie_id>/",
        GetOrderDataByZlecenieAPIView.as_view(),
        name="get orders by id",
    ),
    path("all-orders/", GetAllProductAPIView.as_view(), name="get all orders"),
    path("get-operations/", OperationNameApiView.as_view(), name="get operations name"),
    # database configuration
    path(
        "create-connection/", CreateDatabaseConnectionAPIView.as_view(), name="mssql connection"
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
    path("", include(router.urls)),
]
