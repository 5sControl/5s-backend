from django.urls import path
from .views import (
    FindCameraAPIView, StartDeployment, CheckMemoryStatus
)

urlpatterns = [
    path(
        "deploy/",
        StartDeployment.as_view(),
        name="redirect to go server",
    ),
    path(
        "is_enough_memory/", CheckMemoryStatus.as_view(), name="memory_available",
    ),
    path("find_cameras/", FindCameraAPIView.as_view(), name="find cameras"),
]
