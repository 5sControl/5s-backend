from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Algorithm, CameraAlgorithm
from .serializers import (
    CameraAlgorithmSerializer,
    AlgorithmUpdateSerializer,
    AlgorithmStatusSerializer,
)

from src.StaffControl.Locations.models import Camera

from rest_framework.exceptions import NotFound


class AlgorithmUpdateView(generics.UpdateAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmUpdateSerializer

    def update(self, request, *args, **kwargs):
        received_data = request.data
        for algorithm_name, is_available in received_data.items():
            try:
                algorithm = Algorithm.objects.get(name=algorithm_name)
            except Algorithm.DoesNotExist:
                raise NotFound(
                    detail=f"Algorithm with name '{algorithm_name}' not found"
                )

            algorithm.is_available = is_available
            algorithm.save()

        return Response({"message": "Algorithm status updated"})


class CameraAlgorithmCreateView(generics.CreateAPIView):
    serializer_class = CameraAlgorithmSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        errors = []

        for algorithm_name, camera_ips in data.items():
            algorithm = Algorithm.objects.filter(name=algorithm_name).first()
            if not algorithm:
                errors.append(f"Algorithm with name {algorithm_name} does not exist")
                continue

            if not algorithm.is_available:
                errors.append(f"Algorithm with name {algorithm_name} is not available")
                continue

            cameras = Camera.objects.filter(id__in=camera_ips)
            if not cameras.exists():
                missing_ips = set(camera_ips) - set(
                    cameras.values_list("id", flat=True)
                )
                errors.append(f"Cameras with ip {', '.join(missing_ips)} do not exist")
                continue

            # Check if the exact same record exists
            existing_records = CameraAlgorithm.objects.filter(
                algorithm=algorithm, camera_id__in=cameras.values_list("id", flat=True)
            )

            new_records = [
                CameraAlgorithm(algorithm=algorithm, camera_id=camera)
                for camera in cameras
                if not existing_records.filter(camera_id=camera.id).exists()
            ]

            if new_records:
                # Create new records only if they don't already exist
                CameraAlgorithm.objects.bulk_create(new_records)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "Camera Algorithm records created successfully"}
            )
