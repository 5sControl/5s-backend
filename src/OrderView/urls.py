from django.urls import path
from .views import ZlecenieList, GetAllDataAPIView

urlpatterns = [
    path("", GetAllDataAPIView.as_view(), name="list"),
    path("", ZlecenieList.as_view(), name="test"),
]
