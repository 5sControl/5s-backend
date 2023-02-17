from rest_framework.routers import DefaultRouter
from src.StaffControl.Locations.views import (
    CameraViewSet,
    GateViewSet,
    LocationViewSet,
    PostCameraAPIView,
    GetHttpCamerasLinkAPIView,
    GetRtspCamerasLinkByIpAPIView,
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"camera", CameraViewSet, basename="Camera")
router.register(r"gate", GateViewSet, basename="gates")
router.register(r"location", LocationViewSet, basename="locations")

urlpatterns = [
    path("post_camera/", PostCameraAPIView.as_view()),
    path("get_camera_http_links/", GetHttpCamerasLinkAPIView.as_view()),
    path("get_camera_rtsp_by_ip_links/", GetRtspCamerasLinkByIpAPIView.as_view()),
]

urlpatterns += router.urls
