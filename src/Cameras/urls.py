from src.Cameras.views import (
    GetCameraAPIView,
    PostCameraAPIView,
    GetHttpCamerasLinkAPIView,
    GetRtspCamerasLinkByIpAPIView,
    UpdateCameraAPIView,
)
from django.urls import path


# post
urlpatterns = [
    path("create-camera/", PostCameraAPIView.as_view()),
]
# get
urlpatterns += [
    path("", GetCameraAPIView.as_view()),
    path("get-camera-http-links/", GetHttpCamerasLinkAPIView.as_view()),
    path("get-camera-rtsp-by-ip-links/", GetRtspCamerasLinkByIpAPIView.as_view()),
]
# put/patch
urlpatterns += [
    path("update-camera/", UpdateCameraAPIView.as_view()),
]
