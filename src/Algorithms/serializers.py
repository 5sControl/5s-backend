from rest_framework import serializers

from src.Algorithms.models import CameraAlgorithm
from .models import Algorithm


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ["name"]


class AlgorithmUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = [
            "id",
            "is_available",
        ]


class CameraAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAlgorithm
        fields = ["algorithm", "camera", "is_active", "process_id"]


class AlgorithmStatusSerializer(serializers.Serializer):
    true = AlgorithmSerializer(many=True)
    false = AlgorithmSerializer(many=True)
