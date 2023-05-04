from src.Cameras.views import (
    GetCameraAPIView,
    GetHttpCamerasLinkAPIView,
    GetRtspCamerasLinkByIpAPIView,
    UpdateCameraAPIView,
    PostCameraAPIView,
    DeleteCameraAPIView,
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
# delete
urlpatterns += [path("delete-camera/<str:camera_id>/", DeleteCameraAPIView.as_view())]
