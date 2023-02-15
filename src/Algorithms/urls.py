from django.urls import path
from .views import (
    PutAlgorithmUpdateApiView,
    StartProcessingYoloApiView,
    GetAlgorithmStatusApiView,
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
]
