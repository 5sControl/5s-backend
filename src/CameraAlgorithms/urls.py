from django.urls import path

from .views import (
    CameraAPIView,
    CameraAlgorithmLogListAPIView,
    UpdateCameraAPIView,
    DeleteCameraAPIView,
    CreateCameraAlgorithmsApiView,
    AlgorithmStatusApiView,
    AlgorithmProcessApiView,
    StopProcessApiView,
)

# camera
urlpatterns = [
    path("camera/", CameraAPIView.as_view(), name="camera"),
    path("update-camera/", UpdateCameraAPIView.as_view(), name="camera-update"),
    path(
        "delete_camera/<str:pk>/", DeleteCameraAPIView.as_view(), name="camera-delete"
    ),
    path(
        "create-process/",
        CreateCameraAlgorithmsApiView.as_view(),
        name="camera-algorithm-create",
    ),
    path(
        "available-process/",
        AlgorithmStatusApiView.as_view(),
        name="algorithms-available",
    ),
    path("get-process/", AlgorithmProcessApiView.as_view(), name="camera-process"),
    path("stop-process/", StopProcessApiView.as_view(), name="algorithms-stop-process"),
    path("logs/", CameraAlgorithmLogListAPIView.as_view(), name="log"),
]
