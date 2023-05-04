from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from src.Algorithms.models import Algorithm, CameraAlgorithm, CameraAlgorithmLog
from src.Cameras.models import Camera
from src.Core.paginators import NoPagination

from src.Core.permissions import IsStaffPermission, IsSuperuserPermission

from .services.services import (
    CreateCameraAlgorithms,
    StopCameraAlgorithm,
    UpdateCameraInfo,
    DeleteCamera,
    UpdateStatusAlgorithm,
)
from .serializers import (
    AlgorithmDetailSerializer,
    CameraAlgorithmFullSerializer,
    CameraModelSerializer,
    CreateCameraAlgorithmSerializer,
    StopAlgorithmSerializer,
    UpdateCameraSerializer,
    CameraAlgorithmLogSerializer,
)


class CameraAPIView(generics.ListAPIView):
    serializer_class = CameraModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NoPagination
    queryset = Camera.objects.all()


class AlgorithmDetailApiView(generics.ListAPIView):
    serializer_class = AlgorithmDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Algorithm.objects.all()
    pagination_class = NoPagination


class AlgorithmProcessApiView(generics.ListAPIView):
    serializer_class = CameraAlgorithmFullSerializer
    queryset = CameraAlgorithm.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = NoPagination


class UpdateCameraAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = UpdateCameraSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = UpdateCameraInfo(serializer.validated_data)
        if result["status"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class DeleteCameraAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    queryset = Camera.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        result = DeleteCamera(instance)
        if result["status"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class StopProcessApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = StopAlgorithmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pid = serializer.validated_data["pid"]
        StopCameraAlgorithm(pid)
        UpdateStatusAlgorithm(pid)
        return Response(
            {"status": True, "message": f"PID {pid} was successfully stopped"},
            status=status.HTTP_200_OK,
        )


class CreateCameraAlgorithmsApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = CreateCameraAlgorithmSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateCameraAlgorithmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        data = serializer.validated_data
        CreateCameraAlgorithms(data)
        return Response(status=status.HTTP_201_CREATED)


class CameraAlgorithmLogListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CameraAlgorithmLog.objects.all()
    serializer_class = CameraAlgorithmLogSerializer
