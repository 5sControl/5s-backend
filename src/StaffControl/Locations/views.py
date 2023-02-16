from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.StaffControl.Locations.models import Camera, Gate, Location
from src.StaffControl.Locations.serializers import (
    CameraSerializer,
    GateSerializer,
    LocationSerializer,
)

from .service import link_generator


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


class SaveCameraDetailsAPIView(APIView):
    """Write all camera information"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result = link_generator.create_camera(request.data)
        return Response(result)


class GetHttpCamerasLinkAPIView(APIView):
    """
    Collection of all informations about cameras and create a http link to connect to the camera
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = link_generator.get_camera_http_link()
        return Response({"result": result})


class GetRtspCamerasLinkAPIView(APIView):
    """
    Collection of all informations about cameras and create a rtsp link to connect to the camera
    """

    # permission_classes = [IsAuthenticated] # FIXME:

    def get(self, request, *args, **kwargs):
        result = link_generator.get_camera_rtsp_link()
        return Response({"result": result})


class GetRtspCamerasLinkByIpAPIView(APIView):
    """
    Return one rtsp link by camera ip
    """

    # permission_classes = [IsAuthenticated] # FIXME:

    def post(self, request, *args, **kwargs):
        result = link_generator.get_camera_rtsp_link_by_camera(request.data)
        return Response({"result": result})
