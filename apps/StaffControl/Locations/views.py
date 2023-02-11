from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.StaffControl.Locations.models import Camera, Gate, Location
from apps.StaffControl.Locations.serializers import (
    CameraSerializer,
    GateSerializer,
    LocationSerializer,
)

from .service import save_camera, create_camera_link


class CameraViewSet(ModelViewSet):
    """List of all Camer"""

    serializer_class = CameraSerializer
    queryset = Camera.objects.all()
    permission_classes = [IsAuthenticated]


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


class SaveCameraDetailsView(APIView):
    """Write all camera information"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result = save_camera(request.data)
        return Response(result)


class GetCamerasLink(APIView):
    """
    Collection of all informations about cameras and create a link to connect to the camera
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = create_camera_link()
        return Response({"result": result})
