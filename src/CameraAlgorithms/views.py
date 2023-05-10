from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from src.Algorithms.models import Algorithm, CameraAlgorithm, CameraAlgorithmLog
from src.Cameras.models import Camera
from src.Core.paginators import NoPagination

from src.Core.permissions import IsStaffPermission, IsSuperuserPermission

from .services.cameraalgorithm import (
    CreateCameraAlgorithms,
    DeleteCamera,
)
from .serializers import (
    AlgorithmDetailSerializer,
    CameraAlgorithmFullSerializer,
    CameraModelSerializer,
    CreateCameraAlgorithmSerializer,
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


class CreateCameraAlgorithmsApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = CreateCameraAlgorithmSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateCameraAlgorithmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        CreateCameraAlgorithms(serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class CameraAlgorithmLogListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CameraAlgorithmLog.objects.all()
    serializer_class = CameraAlgorithmLogSerializer
