from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.core.permissions import IsStaffPermission, IsSuperuserPermission

from .models import Algorithm
from .service import algorithms_services
from .utils import yolo_proccesing
from .serializers import (
    AlgorithmUpdateSerializer,
    AlgorithmStatusSerializer,
    CameraAlgorithmFullSerializer,
    CameraAlgorithmSerializer,
)


class PutAlgorithmUpdateApiView(generics.UpdateAPIView):
    """Update status of an algorithm"""

    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmUpdateSerializer

    def update(self, request, *args, **kwargs):
        response = algorithms_services.update_status_of_algorithm(data=request.data)
        return Response(response, status=status.HTTP_200_OK)


class StartProcessingYoloApiView(generics.CreateAPIView):
    """
    A view that handles creation of camera algorithm records and starting YOLO processing.
    """

    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = CameraAlgorithmSerializer

    def create(self, request, *args, **kwargs):
        response = algorithms_services.create_camera_algorithm(data=request.data)
        return Response(response, status=status.HTTP_200_OK)


class GetAlgorithmStatusApiView(generics.GenericAPIView):
    """
    Get the status of  a camera algorithm

    Example response:
    {
        "algorithm": true,
    }
    """

    serializer_class = AlgorithmStatusSerializer

    def get(self, request, *args, **kwargs):
        algorithm_data = algorithms_services.get_algorithms_status()
        return Response(algorithm_data, status=status.HTTP_200_OK)


class GetAlgorithmProcessApiView(generics.GenericAPIView):
    """
    Get all YOLO processes for a camera algorithm
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CameraAlgorithmFullSerializer

    def get(self, request, *args, **kwargs):
        process = algorithms_services.get_camera_algorithms()
        serialized_data = self.serializer_class(process, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class StopProcessApiView(generics.GenericAPIView):
    """Get pid and stop process"""

    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = ...

    def post(self, request, *args, **kwargs):
        pid = request.data["pid"]
        request = yolo_proccesing.stop_process(pid)
        result = algorithms_services.update_status_of_algorithm_by_pid(pid=pid)
        if result["status"] and request["success"]:
            return Response({"status": True, "message": f"PID {pid} was successfully stopped"})
        else:
            return Response({"status": False, "message": f"PID {pid} was not found"})