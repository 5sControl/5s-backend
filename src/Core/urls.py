from django.urls import path
from .views import (
    StartDeployment, CheckMemoryStatus
)

urlpatterns = [
    path(
        "deploy/",
        StartDeployment.as_view(),
        name="redirect to go server",
    ),
    path(
        "is_enough_memory/", CheckMemoryStatus.as_view(), name="memory_available",
    )
]
