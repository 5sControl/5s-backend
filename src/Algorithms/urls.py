from django.urls import path
from .views import (
    AlgorithmUpdateView,
    CameraAlgorithmCreateView,
    AlgorithmStatusView,
)

urlpatterns = [
    path("update/", AlgorithmUpdateView.as_view(), name="algorithm-update"),
    path("create/", CameraAlgorithmCreateView.as_view(), name="algorithm-create"),
    path(
        "available/",
        AlgorithmStatusView.as_view(),
        name="algorithms-available",
    ),
]
