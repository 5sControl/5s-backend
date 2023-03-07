from django.urls import path
from .views import (
    GetAllDataAPIView,
)

urlpatterns = [
    path("/", GetAllDataAPIView.as_view(), name="list"),
]
