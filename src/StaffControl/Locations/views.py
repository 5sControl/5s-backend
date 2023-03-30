from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from src.StaffControl.Locations.models import Gate, Location
from src.StaffControl.Locations.serializers import (
    GateSerializer,
    LocationSerializer,
)
from src.StaffControl.Locations.models import Gate, Location
from src.StaffControl.Locations.serializers import GateSerializer, LocationSerializer


class GateViewSet(ModelViewSet):
    """List of all gates"""

    serializer_class = GateSerializer
    queryset = Gate.objects.all()
    permission_classes = [IsAuthenticated]


class LocationViewSet(ModelViewSet):
    """List of all locations"""

    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = [IsAuthenticated]
