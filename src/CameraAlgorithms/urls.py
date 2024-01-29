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
    ZoneCameraListView,
    CameraZoneAlgorithmView,
    UniqueImageNameView,
    AlgorithmInfoView,
    UploadAlgorithmView,
    DecryptDataView,
)

router = DefaultRouter()
router.register(r"zone", ZoneCameraListAPIView, basename="ZoneCameraList")
router.register(r"algorithms-detail", AlgorithmDetailApiView, basename="algorithms-available")


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
    path("get-process/", AlgorithmProcessApiView.as_view(), name="camera-process"),
    path("logs/", CameraAlgorithmLogListAPIView.as_view(), name="log"),
    path("zone-cameras/", ZoneCameraListView.as_view(), name="zone-cameras"),
    path(
        "zones-algorithms/", CameraZoneAlgorithmView.as_view(), name="algorithms-zone"
    ),
    path('unique-image-names/', UniqueImageNameView.as_view(), name='unique-image-names'),
    path('algorithm-info/', AlgorithmInfoView.as_view(), name='algorithm-info'),
    path('upload-algorithm/<int:id_algorithm>/', UploadAlgorithmView.as_view(), name='upload-algorithm'),
    path('decrypt/', DecryptDataView.as_view(), name='decrypt_data'),

]

urlpatterns += router.urls
