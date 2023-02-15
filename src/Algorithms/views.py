from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Algorithm
from .service import algorithms_services
from .serializers import (
    CameraAlgorithmSerializer,
    AlgorithmUpdateSerializer,
    AlgorithmStatusSerializer,
)


class PutAlgorithmUpdateApiView(generics.UpdateAPIView):
    """Update status of an algorithm"""

    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmUpdateSerializer

    def update(self, request, *args, **kwargs):
        response = algorithms_services.update_status_of_algorithm(data=request.data)
        return Response(response)


class StartProcessingYoloApiView(generics.CreateAPIView):
    """
    A view that handles creation of camera algorithm records and starting YOLO processing.
    """

    serializer_class = CameraAlgorithmSerializer

    def create(self, request, *args, **kwargs):
        response = algorithms_services.create_camera_algorithm(data=request.data)
        return Response(response)


class GetAlgorithmStatusApiView(generics.GenericAPIView):
    """
    Get the status of a camera algorithm

    Example response:
    {
        "algorithm": true,
    }
    """

    serializer_class = AlgorithmStatusSerializer

    def get(self, request, *args, **kwargs):
        algorithm_data = algorithms_services.get_algorithms_status()
        return Response(algorithm_data, status=status.HTTP_200_OK)
