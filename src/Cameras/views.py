from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.Cameras.models import Camera
from src.Cameras.serializers import CameraSerializer

from .service import link_generator


class CameraViewSet(ModelViewSet):
    """List of all Cameras"""

    serializer_class = CameraSerializer
    queryset = Camera.objects.all()
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
