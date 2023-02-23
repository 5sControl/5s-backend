from rest_framework import serializers

from src.Algorithms.models import CameraAlgorithm
from src.Cameras.serializers import CameraProcessSerializer

from .models import Algorithm


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ("id", "name")


class AlgorithmUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = [
            "id",
            "is_available",
        ]


class AlgorithmStatusSerializer(serializers.Serializer):
    true = AlgorithmSerializer(many=True)
    false = AlgorithmSerializer(many=True)


class CameraAlgorithmFullSerializer(serializers.ModelSerializer):
    algorithm = AlgorithmSerializer()
    camera = CameraProcessSerializer()

    class Meta:
        model = CameraAlgorithm
        fields = ["camera", "algorithm", "process_id", "is_active"]
