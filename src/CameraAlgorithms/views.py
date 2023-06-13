from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from src.Core.paginators import NoPagination
from src.Core.permissions import IsStaffPermission, IsSuperuserPermission

from .models import Camera, ZoneCameras
from .models import Algorithm, CameraAlgorithm, CameraAlgorithmLog
from .services.cameraalgorithm import (
    CreateCameraAlgorithms,
    DeleteCamera,
)
from .serializers import (
    AlgorithmDetailSerializer,
    CameraAlgorithmFullSerializer,
    CameraModelSerializer,
    CreateCameraAlgorithmSerializer,
    CameraAlgorithmLogSerializer, ZoneCameraSerializer,
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
        return Response(result, status=status.HTTP_200_OK)


class CreateCameraAlgorithmsApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = CreateCameraAlgorithmSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateCameraAlgorithmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CreateCameraAlgorithms(serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class CameraAlgorithmLogListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CameraAlgorithmLog.objects.all()
    serializer_class = CameraAlgorithmLogSerializer


class ZoneCameraListAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = NoPagination
    queryset = ZoneCameras.objects.all()
    serializer_class = ZoneCameraSerializer


class ZoneCameraListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        camera_id = request.GET.get('camera')
        queryset = CameraAlgorithm.objects.filter(camera_id=camera_id) if camera_id else CameraAlgorithm.objects.all()

        algorithms = {}

        for camera_algorithm in queryset:
            algorithm_name = camera_algorithm.algorithm.name
            zones = camera_algorithm.zones
            zone_ids = [zone['id'] for zone in zones] if zones else []
            if algorithm_name in algorithms:
                algorithms[algorithm_name].extend(zone_ids)
            else:
                algorithms[algorithm_name] = zone_ids

        response_data = {
            'camera': camera_id,
            'algorithms': algorithms
        }

        return Response(response_data)
