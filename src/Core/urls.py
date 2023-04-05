from django.urls import path
from .views import (
    StartDeployment
)

urlpatterns = [
    path(
        "deploy/",
        StartDeployment.as_view(),
        name="redirect to go server",
    ),
]