from rest_framework import serializers

from src.Algorithms.models import CameraAlgorithm
from src.Cameras.serializers import CameraProcessSerializer

from .models import Algorithm, CameraAlgorithmLog


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

    class Meta:
        ref_name = "algorithm_status"


class CameraAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAlgorithm
        fields = ["algorithm", "camera", "is_active", "process_id"]


class CameraAlgorithmFullSerializer(serializers.ModelSerializer):
    algorithm = AlgorithmSerializer()
    camera = CameraProcessSerializer()

    class Meta:
        model = CameraAlgorithm
        fields = ["camera", "algorithm", "process_id", "is_active"]


class CameraAlgorithmLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAlgorithmLog
        fields = "__all__"
