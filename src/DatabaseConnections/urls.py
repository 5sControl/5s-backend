from django.urls import path

from .views import ActiveResourceView


urlpatterns = [
    path("status/", ActiveResourceView.as_view(), name="connector-status"),
]
