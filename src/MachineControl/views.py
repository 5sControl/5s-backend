from rest_framework.viewsets import ModelViewSet
from src.MachineControl.models import MachineAction
from src.MachineControl.serializers import MachineControlSerializers
from rest_framework.permissions import IsAuthenticated


class MachineControlViewSet(ModelViewSet):
    """List of all Actions on MachineControl"""

    serializer_class = MachineControlSerializers
    queryset = MachineAction.objects.all()
    # permission_classes = [IsAuthenticated]
