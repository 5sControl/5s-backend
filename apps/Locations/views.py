from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from apps.Employees.models import CustomUser
from apps.Locations.serializers import CameraSerializer, GateSerializer, LocationSerializer


class CameraViewSet(ModelViewSet):
    """List of all cameras"""
    serializer_class = CameraSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class GateViewSet(ModelViewSet):
    """List of all gates"""
    serializer_class = GateSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class LocationViewSet(ModelViewSet):
    """List of all locations"""
    serializer_class = LocationSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
