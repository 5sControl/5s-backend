from rest_framework.routers import DefaultRouter
from src.MachineControl.views import MachineControlViewSet


router_machine = DefaultRouter()

router_machine.register(r"action", MachineControlViewSet, basename="actions")

urlpatterns = router_machine.urls
