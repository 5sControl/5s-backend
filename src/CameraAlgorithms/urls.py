from django.urls import path

from .views import (
    CameraAPIView,
    CameraAlgorithmLogListAPIView,
    DeleteCameraAPIView,
    CreateCameraAlgorithmsApiView,
    CameraCheckConnection,
    AlgorithmDetailApiView,
    AlgorithmProcessApiView,
)


urlpatterns = [
    path("camera/", CameraAPIView.as_view(), name="camera"),
    path(
        "camera/check-connection/",
        CameraCheckConnection.as_view(),
        name="check-connection",
    ),
    path(
        "delete-camera/<str:pk>/", DeleteCameraAPIView.as_view(), name="camera-delete"
    ),
    path(
        "create-process/",
        CreateCameraAlgorithmsApiView.as_view(),
        name="camera-algorithm-create",
    ),
    path(
        "algorithms-detail/",
        AlgorithmDetailApiView.as_view(),
        name="algorithms-available",
    ),
    path("get-process/", AlgorithmProcessApiView.as_view(), name="camera-process"),
    path("logs/", CameraAlgorithmLogListAPIView.as_view(), name="log"),
]
