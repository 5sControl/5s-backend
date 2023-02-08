from rest_framework.routers import DefaultRouter
from apps.Locations.views import (
    CameraViewSet,
    GateViewSet,
    LocationViewSet,
    GetOnvifCameraView,
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"camera", CameraViewSet, basename="Camera")
router.register(r"gate", GateViewSet, basename="gates")
router.register(r"location", LocationViewSet, basename="locations")

urlpatterns = [
    path("get_all_cameras/", GetOnvifCameraView.as_view()),
]

urlpatterns += router.urls
