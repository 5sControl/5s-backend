from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from apps.Locations.models import Camera, Gate, Location

from apps.Locations.serializers import CameraSerializer, GateSerializer, LocationSerializer


class CameraViewSet(ModelViewSet):
    """List of all Camer"""

    serializer_class = CameraSerializer
    queryset = Camera.objects.all()

    permission_classes_by_action = {'get': [permissions.AllowAny],
                                    'update': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated]}

class GateViewSet(ModelViewSet):
    """List of all gates"""

    serializer_class = GateSerializer
    queryset = Gate.objects.all()

    permission_classes_by_action = {'get': [permissions.AllowAny],
                                    'update': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated]}

class LocationViewSet(ModelViewSet):
    """List of all locations"""

    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    permission_classes_by_action = {'get': [permissions.AllowAny],
                                    'update': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated]}