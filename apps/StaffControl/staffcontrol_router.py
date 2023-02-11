from rest_framework.routers import DefaultRouter

from django.urls import path, include
from django.urls import path

router = DefaultRouter()


routes_staff = [
    path("employees/", include("apps.StaffControl.Employees.urls")),
    path("locations/", include("apps.StaffControl.Locations.urls")),
    path("history/", include("apps.StaffControl.History.urls")),
]

urlpatterns = routes_staff
