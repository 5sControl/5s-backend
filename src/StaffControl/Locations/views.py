import cv2
import base64

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


class SaveCameraDetailsView(APIView):
    """Write all camera information"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result = link_generator.create_camera(request.data)
        return Response(result)


class GetCamerasLink(APIView):
    """
    Collection of all informations about cameras and create a link to connect to the camera
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = link_generator.get_camera_http_link()
        return Response({"result": result})


class GetCameraImagesAPIView(APIView):
    """
    Get all rtsp cameras link and return image from each camera
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = link_generator.get_camera_rtsp_link()
        frames = {}
        for camera_link in result:
            # FIXME: Get correct password from client. Delete replace
            cap = cv2.VideoCapture(
                camera_link["link"].replace(":admin@", ":just4Taqtile@")
            )

            ret, frame = cap.read()
            if ret:
                retval, buffer = cv2.imencode(".jpg", frame)
                encoded_image = base64.b64encode(buffer).decode("utf-8")

                frames[camera_link["ip"]] = encoded_image

        return Response(frames)
