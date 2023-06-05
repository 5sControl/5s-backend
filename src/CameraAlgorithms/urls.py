from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    CameraAPIView,
    CameraAlgorithmLogListAPIView,
    DeleteCameraAPIView,
    CreateCameraAlgorithmsApiView,
    AlgorithmDetailApiView,
    AlgorithmProcessApiView,
    ZoneCameraListAPIView,
)

router = DefaultRouter()
router.register(r"zone", ZoneCameraListAPIView, basename="ZoneCameraList")


urlpatterns = [
    path("camera/", CameraAPIView.as_view(), name="camera"),
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

urlpatterns += router.urls
