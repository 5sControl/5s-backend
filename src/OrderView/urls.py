from django.urls import path
from .views import GetAllDataAPIView, ZlecenieList

urlpatterns = [
    path("", GetAllDataAPIView.as_view(), name="list"),
]
