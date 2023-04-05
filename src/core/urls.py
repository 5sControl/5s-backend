from django.urls import path
from .views import (
    StartDeployment
)

urlpatterns = [
    path(
        "deploy/<str:zlecenie_id>/",
        StartDeployment.as_view(),
        name="redirect to go server",
    ),
]