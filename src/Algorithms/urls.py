from django.urls import path
from .views import (
    AlgorithmUpdateApiView,
    StartProcessingYoloApiView,
    GetAlgorithmStatusApiView,
    GetAlgorithmProcessApiView,
    StopProcessApiView,
    CameraAlgorithmLogListAPIView,
)

urlpatterns = [
    path("update/", AlgorithmUpdateApiView.as_view(), name="algorithm-update"),
    path(
        "create-process/",
        StartProcessingYoloApiView.as_view(),
        name="algorithm-create",
    ),
    path(
        "available-process/",
        GetAlgorithmStatusApiView.as_view(),
        name="algorithms-available",
    ),
    path(
        "get-process/", GetAlgorithmProcessApiView.as_view(), name="camera-get-process"
    ),
    path("stop-process/", StopProcessApiView.as_view(), name="stop-process"),
    path("logs/", CameraAlgorithmLogListAPIView.as_view(), name="log"),
]
