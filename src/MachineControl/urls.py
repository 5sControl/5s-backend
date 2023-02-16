from rest_framework.routers import DefaultRouter
from django.urls import path
from src.MachineControl.views import MachineControlViewSet, MachineActionListView


router_machine = DefaultRouter()

router_machine.register(r"action", MachineControlViewSet, basename="actions")
# router_machine.register(r"action_camera", MachineActionListView, basename="actions_cameras")


urlpatterns = [
    path('machine_actions/', MachineActionListView.as_view(), name='machine_action_list'),
]

urlpatterns += router_machine.urls
