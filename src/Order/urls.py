from django.urls import path
from .views import (
    GetOrderApiView,
    DatabaseConnectionApiView,
)

urlpatterns = [
    path("", GetOrderApiView.as_view(), name="get-order"),
    path("connect/", DatabaseConnectionApiView.as_view(), name="db-connection"),
]
