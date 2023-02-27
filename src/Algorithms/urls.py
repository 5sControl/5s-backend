from django.urls import path
from .views import (
    PutAlgorithmUpdateApiView,
    StartProcessingYoloApiView,
    GetAlgorithmStatusApiView,
    GetAlgorithmProcessApiView,
    StopProcessApiView,
)

urlpatterns = [
    path("update/", PutAlgorithmUpdateApiView.as_view(), name="algorithm-update"),
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
]
