from rest_framework import generics
from rest_framework.response import Response

from .models import Algorithm, CameraAlgorithm
from .serializers import CameraAlgorithmSerializer, AlgorithmUpdateSerializer


class AlgorithmUpdateView(generics.UpdateAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmUpdateSerializer

    def update(self, request, *args, **kwargs):
        received_data = request.data
        for key, value in received_data.items():
            algorithm = Algorithm.objects.get(id=key)
            algorithm.is_available = value
            algorithm.save()

        return Response({"message": "Algorithm status updated"})


class CameraAlgorithmCreateView(generics.CreateAPIView):
    queryset = CameraAlgorithm.objects.all()
    serializer_class = CameraAlgorithmSerializer
