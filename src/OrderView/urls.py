from django.urls import path
from .views import GetAllDataAPIView, ZleceniaListView

urlpatterns = [
    path("", GetAllDataAPIView.as_view(), name="list"),
    path("test/", ZleceniaListView.as_view)
]
