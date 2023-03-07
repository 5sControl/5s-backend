from django.urls import path
from .views import (
    GetOrderApiView,
)

urlpatterns = [
    path("", GetOrderApiView.as_view(), name="get-order"),
]
