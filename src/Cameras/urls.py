from src.Cameras.views import (
    GetCameraAPIView,
    GetHttpCamerasLinkAPIView,
    GetRtspCamerasLinkByIpAPIView,
    CreateCameraAPIView,
    UpdateCameraAPIView,
    DeleteCameraAPIView,
)

from django.urls import path


urlpatterns = [
    path("", GetCameraAPIView.as_view(), name="camera"),
    path("get-camera-http-links/", GetHttpCamerasLinkAPIView.as_view(), name="http-links"),
    path("get-camera-rtsp-by-ip-links/", GetRtspCamerasLinkByIpAPIView.as_view(), name="rtsp-by-ip-links"),
    path("create-camera/", CreateCameraAPIView.as_view(), name="create-camera"),
    path("update-camera/", UpdateCameraAPIView.as_view(), name="update-camera"),
    path('delete_camera/<str:pk>/', DeleteCameraAPIView.as_view(), name="delete-camera"),
]
