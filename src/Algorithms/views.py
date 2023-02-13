from rest_framework import generics
from rest_framework.response import Response

from .models import Algorithm, CameraAlgorithm
from .serializers import CameraAlgorithmSerializer, AlgorithmUpdateSerializer

from src.StaffControl.Locations.models import Camera

from django.core.exceptions import ValidationError


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
    serializer_class = CameraAlgorithmSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        for algorithm_name, camera_ips in data.items():
            algorithm = Algorithm.objects.filter(name=algorithm_name).first()
            if not algorithm:
                raise ValidationError(
                    {"error": f"Algorithm with name {algorithm_name} does not exists"}
                )

            cameras = Camera.objects.filter(id__in=camera_ips)
            if not cameras.exists():
                missing_ips = set(camera_ips) - set(
                    cameras.values_list("id", flat=True)
                )
                raise ValidationError(
                    {"error": f"Cameras with ip {', '.join(missing_ips)} do not exist"}
                )

            CameraAlgorithm.objects.bulk_create(
                [
                    CameraAlgorithm(algorithm=algorithm, camera_id=camera)
                    for camera in cameras
                ]
            )

        return Response({"message": "Camera Algorithm records created successfully"})
