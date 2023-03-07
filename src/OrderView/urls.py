from django.urls import path
from .views import GetAllDataListAPIView

urlpatterns = [
    path("", GetAllDataListAPIView.as_view(), name="list"),
]
