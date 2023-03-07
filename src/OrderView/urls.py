from django.urls import path
from .views import (
    GetAllDataListApiView,
)

urlpatterns = [
    path("/", GetAllDataListApiView.as_view(), name="list"),
]
