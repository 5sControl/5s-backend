from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from src.Core.permissions import IsStaffPermission, IsSuperuserPermission

from .models.camera import Camera
from .models.algorithm import Algorithm, CameraAlgorithm, CameraAlgorithmLog
from .services.services import (
    CreateCameraAlgorithms,
    StopCameraAlgorithm,
    UpdateCameraInfo,
    DeleteCamera,
    UpdateStatusAlgorithm,
)
from .serializers import (
    AlgorithmStatusSerializer,
    CameraAlgorithmFullSerializer,
    CameraModelSerializer,
    CameraSerializer,
    StopAlgorithmSerializer,
    UpdateCameraSerializer,
    CameraAlgorithmLogSerializer,
)


class CameraAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Camera.objects.all()
    serializer_class = CameraModelSerializer


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


class AlgorithmStatusApiView(generics.GenericAPIView):
    serializer_class = AlgorithmStatusSerializer

    def get(self, request, *args, **kwargs):
        algorithms = Algorithm.objects.all()
        algorithm_data = {
            algorithm.name: algorithm.is_available for algorithm in algorithms
        }
        return Response(algorithm_data, status=status.HTTP_200_OK)


class AlgorithmProcessApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CameraAlgorithmFullSerializer

    def get(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(
            CameraAlgorithm.objects.all(), many=True
        )
        return Response(serialized_data.data, status=status.HTTP_200_OK)


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
    serializer_class = CameraSerializer

    def post(self, request, *args, **kwargs):
        serializer = CameraSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        CreateCameraAlgorithms(data)
        return Response(status=status.HTTP_201_CREATED)


class CameraAlgorithmLogListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CameraAlgorithmLog.objects.all()
    serializer_class = CameraAlgorithmLogSerializer
