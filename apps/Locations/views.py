from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from apps.Locations.models import Camera, Gate, Location

from apps.Locations.serializers import CameraSerializer, GateSerializer, LocationSerializer
from apps.base.permissions import IsAdminOrReadOnly

class CameraViewSet(ModelViewSet):
    """List of all Camer"""

    serializer_class = CameraSerializer
    queryset = Camera.objects.all()

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,]


class GateViewSet(ModelViewSet):
    """List of all gates"""

    serializer_class = GateSerializer
    queryset = Gate.objects.all()

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,]

class LocationViewSet(ModelViewSet):
    """List of all locations"""

    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,]