from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.Locations.models import Camera, Gate, Location
from apps.Locations.serializers import (
    CameraSerializer,
    GateSerializer,
    LocationSerializer,
)


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


class PostCameraView(APIView):
    """Write all camera information"""

    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            list_of_ips = request.data["cameras_ip"]
            for ip in list_of_ips:
                camera = Camera(id=ip)
                camera.save()
                print(f"Camera {ip} was successfully saved")
            return Response({"status": "success"})
        except KeyError as e:
            return Response({"status": "failure", "error": f"KeyError: {str(e)}"})
        except Exception as e:
            return Response({"status": "failure", "error": f"Exception: {str(e)}"})
