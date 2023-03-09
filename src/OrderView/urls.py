from django.urls import path
from .views import GetAllDataAPIView, ZleceniaSkansAPIView

urlpatterns = [
    path("", GetAllDataAPIView.as_view(), name="list"),
    path("test/", ZleceniaSkansAPIView.as_view())
]
