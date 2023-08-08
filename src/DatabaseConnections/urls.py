from django.urls import path

from .views import UpdateActiveResourceView


urlpatterns = [
    path(
        "status/",
        UpdateActiveResourceView.as_view(),
        name="connector-status",
    )
]
