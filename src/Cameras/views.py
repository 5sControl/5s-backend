from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from src.Core.permissions import IsStaffPermission, IsSuperuserPermission

from src.Cameras.models import Camera
from src.Cameras.serializers import (
    CameraSerializer,
    CreateCameraSerializer,
    UpdateCameraSerializer
)
from src.Cameras.services.camera_services import camera_service
from src.Cameras.services.link_generator import link_generator


class GetCameraAPIView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class GetHttpCamerasLinkAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = link_generator.get_camera_http_link()
        return Response(data={"result": result}, status=status.HTTP_200_OK)


class GetRtspCamerasLinkByIpAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        result = link_generator.get_camera_rtsp_link_by_camera(request.data)
        return Response(data={"result": result}, status=status.HTTP_200_OK)


class CreateCameraAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = CreateCameraSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = camera_service.create_camera(serializer.validated_data)
        if not result["status"]:
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=result, status=status.HTTP_201_CREATED)


class DeleteCameraAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    queryset = Camera.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        result = camera_service.delete_camera(instance)
        if result["status"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class UpdateCameraAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = UpdateCameraSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = camera_service.update_camera_info(serializer.validated_data)
        if result["status"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
