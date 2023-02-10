from rest_framework.routers import DefaultRouter
from apps.Locations.views import (
    CameraViewSet,
    GateViewSet,
    LocationViewSet,
    PostCameraView,
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"camera", CameraViewSet, basename="Camera")
router.register(r"gate", GateViewSet, basename="gates")
router.register(r"location", LocationViewSet, basename="locations")

urlpatterns = [
    path("post_camera/", PostCameraView.as_view()),
]

urlpatterns += router.urls
