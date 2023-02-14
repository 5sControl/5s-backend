from rest_framework.routers import DefaultRouter
from src.MachineControl.views import MachineControlViewSet
from django.urls import path, include

router_machine = DefaultRouter()

router_machine.register(r"actions", MachineControlViewSet, basename="Actions")

urlpatterns = router_machine.urls
