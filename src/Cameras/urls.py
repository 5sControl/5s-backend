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
    path("", GetCameraAPIView.as_view()),
    path("get-camera-http-links/", GetHttpCamerasLinkAPIView.as_view()),
    path("get-camera-rtsp-by-ip-links/", GetRtspCamerasLinkByIpAPIView.as_view()),
    path("create-camera/", CreateCameraAPIView.as_view()),
    path("update-camera/", UpdateCameraAPIView.as_view()),
    path('delete_camera/<str:pk>/', DeleteCameraAPIView.as_view()),
]
