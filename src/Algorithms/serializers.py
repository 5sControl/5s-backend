from rest_framework import serializers

from src.Algorithms.models import CameraAlgorithm
from .models import Algorithm

from django.core.exceptions import ValidationError


class AlgorithmUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = [
            "id",
            "is_available",
        ]


class CameraAlgorithmSerializer(serializers.ModelSerializer):
    algorithm = serializers.CharField(write_only=True)

    class Meta:
        model = CameraAlgorithm
        fields = ("algorithm", "camera_id")

    def create(self, validated_data):
        algorithm_name = validated_data.pop("algorithm")
        algorithm = Algorithm.objects.get(name=algorithm_name)
        if algorithm:
            validated_data["algorithm"] = algorithm
            camera_algorithm = CameraAlgorithm.objects.create(**validated_data)
            return camera_algorithm
        else:
            raise ValidationError(
                {"error": f"Algorithm with name {algorithm_name} does not exists"}
            )
