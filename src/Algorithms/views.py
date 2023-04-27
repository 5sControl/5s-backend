from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.Core.permissions import IsStaffPermission, IsSuperuserPermission

from src.Algorithms.models import Algorithm
from src.Algorithms.services.edit_algorithms import edit_algorithms
from src.Algorithms.services.get_services import algorithms_detail
from src.Algorithms.services.logs_algorithms import logs_service
from src.Algorithms.utils import yolo_proccesing
from src.Algorithms.serializers import (
    AlgorithmUpdateSerializer,
    AlgorithmStatusSerializer,
    CameraAlgorithmFullSerializer,
    CameraAlgorithmLogSerializer,
    CameraAlgorithmSerializer,
)


class AlgorithmUpdateApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmUpdateSerializer

    def update(self, request, *args, **kwargs):
        response = edit_algorithms.update_status_of_algorithm(data=request.data)
        return Response(response, status=status.HTTP_200_OK)


class StartProcessingYoloApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = CameraAlgorithmSerializer

    def create(self, request, *args, **kwargs):
        response = edit_algorithms.create_camera_algorithm(data=request.data)
        if not response["status"]:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)


class GetAlgorithmStatusApiView(generics.GenericAPIView):
    serializer_class = AlgorithmStatusSerializer

    def get(self, request, *args, **kwargs):
        algorithm_data = algorithms_detail.get_algorithms_status()
        return Response(algorithm_data, status=status.HTTP_200_OK)


class GetAlgorithmProcessApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CameraAlgorithmFullSerializer

    def get(self, request, *args, **kwargs):
        process = algorithms_detail.get_camera_algorithms()
        serialized_data = self.serializer_class(process, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class StopProcessApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]

    def post(self, request, *args, **kwargs):
        pid = request.data["pid"]
        request = yolo_proccesing.stop_process(pid)
        result = edit_algorithms.update_status_of_algorithm_by_pid(pid=pid)
        if result["status"] and request["success"]:
            return Response(
                {"status": True, "message": f"PID {pid} was successfully stopped"}
            )
        else:
            return Response({"status": False, "message": f"PID {pid} was not found"})


class CameraAlgorithmLogListAPIView(generics.ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    queryset = logs_service.get_logs()
    serializer_class = CameraAlgorithmLogSerializer
