from django.urls import path
from .views import (
    PutAlgorithmUpdateApiView,
    StartProcessingYoloApiView,
    GetAlgorithmStatusApiView,
    GetAlgorithmProcessApiView,
)

urlpatterns = [
    path("update/", PutAlgorithmUpdateApiView.as_view(), name="algorithm-update"),
    path(
        "create_process/",
        StartProcessingYoloApiView.as_view(),
        name="algorithm-create",
    ),
    path(
        "available/",
        GetAlgorithmStatusApiView.as_view(),
        name="algorithms-available",
    ),
    path(
        "get_process/", GetAlgorithmProcessApiView.as_view(), name="camera-get_process"
    ),
]
