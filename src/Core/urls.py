from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import FindCameraAPIView, SystemMessagesApiView

api_router = DefaultRouter()

api_router.register('system-message', SystemMessagesApiView, basename='system-message')

urlpatterns = [
    path('', include(api_router.urls)),
    path("find_cameras/", FindCameraAPIView.as_view(), name="find-cameras"),
]
