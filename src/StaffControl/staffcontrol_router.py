from rest_framework.routers import DefaultRouter

from django.urls import path, include
from django.urls import path

router = DefaultRouter()


routes_staff = [
    path("employees/", include("src.StaffControl.Employees.urls")),
    path("locations/", include("src.StaffControl.Locations.urls")),
    path("history/", include("src.StaffControl.History.urls")),
]

urlpatterns = routes_staff
