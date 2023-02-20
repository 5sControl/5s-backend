from django.urls import path, include

from django.urls import path

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


routes_staff = [
    path("safety/", include("src.SafetyControl.urls")),
]

urlpatterns = routes_staff
