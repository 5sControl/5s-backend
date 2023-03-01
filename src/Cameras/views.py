from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from src.Cameras.models import Camera
from src.Cameras.serializers import (
    CameraSerializer,
)
from src.Cameras.utils import zip_maker
from src.core.permissions import IsStaffPermission, IsSuperuserPermission

from .service import link_generator, camera_service


class GetCameraAPIView(APIView):
    """Get all cameras"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cameras = Camera.objects.all()
        serializer = CameraSerializer(cameras, many=True)
        return Response(serializer.data)


class PostCameraAPIView(APIView):
    """
    This method will create a camera,
    if it is possible to get a snapshot with the received data,
    otherwise an error will be returned
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result = camera_service.create_camera(request.data)
        return Response(result)


class UpdateCameraAPIView(APIView):
    """
    After successfully creating a camera, set name and description
    """
    
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]

    def patch(self, request, *args, **kwargs):
        camera_data = request.data
        result = camera_service.update_camera_info(camera_data)
        return Response(result)


class GetHttpCamerasLinkAPIView(APIView):
    """
    Collection of all informations about cameras and create a http link to connect to the camera
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = link_generator.get_camera_http_link()
        return Response({"result": result})


class GetRtspCamerasLinkByIpAPIView(APIView):
    """
    Return one rtsp link by camera ip
    """

    # permission_classes = [IsAuthenticated] # FIXME

    def post(self, request, *args, **kwargs):
        result = link_generator.get_camera_rtsp_link_by_camera(request.data)
        return Response({"result": result})
    

class GetDataAPIView(APIView):
    """Make zip"""

    def post(self, request, *args, **kwargs):
        algorithm = request.data['algorithm']
        result = zip_maker.create_zip(algorithm)
        return Response(result)
