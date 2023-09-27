from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from src.Core.paginators import NoPagination
from src.Core.permissions import IsStaffPermission, IsSuperuserPermission

from .models import Camera, ZoneCameras
from src.CameraAlgorithms.models import Algorithm, CameraAlgorithm, CameraAlgorithmLog
from .services.tasks import uploading_algorithm
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
    ZoneCameraSerializer,
    UniqueImageNameSerializer,
    AlgorithmInfoSerializer,
)


class CameraAPIView(generics.ListAPIView):
    serializer_class = CameraModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NoPagination
    queryset = Camera.objects.all().order_by('id')


class AlgorithmDetailApiView(ModelViewSet):
    serializer_class = AlgorithmDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Algorithm.objects.all().exclude(is_available=False).order_by('name')
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
        """Creates a separate camera and camera/algorithm"""
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
        camera_ip = request.GET.get("camera")
        queryset = (
            ZoneCameras.objects.filter(camera=camera_ip)
            if camera_ip
            else ZoneCameras.objects.all()
        )
        serializer = ZoneCameraSerializer(queryset, many=True)
        return Response(serializer.data)


class CameraZoneAlgorithmView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        camera_id = request.GET.get("camera")
        queryset = (
            CameraAlgorithm.objects.filter(camera_id=camera_id)
            if camera_id
            else CameraAlgorithm.objects.all()
        )

        algorithms = {}

        for camera_algorithm in queryset:
            algorithm_name = camera_algorithm.algorithm.name
            zones = camera_algorithm.zones
            zone_ids = [zone["id"] for zone in zones] if zones else []
            if algorithm_name in algorithms:
                algorithms[algorithm_name].extend(zone_ids)
            else:
                algorithms[algorithm_name] = zone_ids

        response_data = {"camera": camera_id, "algorithms": algorithms}

        return Response(response_data)


class UniqueImageNameView(APIView):
    """Getting unique container names"""
    def get(self, request, format=None):
        serializer = UniqueImageNameSerializer()
        data = serializer.get_unique_image_names(None)
        return Response(data, status=status.HTTP_200_OK)


class AlgorithmInfoView(APIView):
    def get_queryset(self):
        return Algorithm.objects.exclude(image_name=None)

    def get(self, request, format=None):
        algorithms = self.get_queryset()
        serializer = AlgorithmInfoSerializer(algorithms, many=True)

        additional_data = {
            "name": "5S Control version",
            "version": "v0.5.4",
            "date": "09.27.2023",
            "description": ""
        }

        data = serializer.data
        data.append(additional_data)

        return Response(reversed(data), status=status.HTTP_200_OK)


class UploadAlgorithmView(APIView):
    def post(self, request, id_algorithm: int, format=None):

        algorithm = Algorithm.objects.get(id=id_algorithm)
        uploading_algorithm.apply_async((algorithm.id, algorithm.image_name))

        return Response({"message": "File upload started"}, status=status.HTTP_202_ACCEPTED)
