from rest_framework.viewsets import ModelViewSet
from models import Action
from serializers import MachineControlSerializers
from rest_framework.permissions import IsAuthenticated


class MachineControlViewSet(ModelViewSet):
    """List of all Actions on MachineControl"""

    serializer_class = MachineControlSerializers
    queryset = Action.objects.all()
    # permission_classes = [IsAuthenticated]
