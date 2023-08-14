from django.urls import path

from .views import GetHealthCheckApiView

urlpatterns = [
    path('/', GetHealthCheckApiView.as_view(), name="health_check"),
]
