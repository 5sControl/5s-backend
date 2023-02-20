from rest_framework.routers import DefaultRouter
from src.Cameras.views import (
    CameraViewSet,
    SaveCameraDetailsView,
    GetCamerasLink,
)
from django.urls import path

router = DefaultRouter()

router.register(r"camera", CameraViewSet, basename="Camera")


urlpatterns = [
    path("post_camera/", SaveCameraDetailsView.as_view()),
    path("get_camera_links/", GetCamerasLink.as_view()),
]

urlpatterns += router.urls
