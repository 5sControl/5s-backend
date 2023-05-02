from rest_framework import serializers

from src.Algorithms.models import CameraAlgorithm
from src.Cameras.serializers import CameraProcessSerializer

from .models import Algorithm, CameraAlgorithmLog


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        ref_name = "algortihms-ser"
        fields = ("id", "name")


class AlgorithmUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        ref_name = "algortihms-updates"
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
        ref_name = "camera_algorithm"
        fields = ["algorithm", "camera", "is_active", "process_id"]


class CameraAlgorithmFullSerializer(serializers.ModelSerializer):
    algorithm = AlgorithmSerializer()
    camera = CameraProcessSerializer()

    class Meta:
        model = CameraAlgorithm
        ref_name = "camera-algorithm-full"
        fields = ["camera", "algorithm", "process_id", "is_active"]


class CameraAlgorithmLogSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "camera-algorithm-log"
        model = CameraAlgorithmLog
        fields = "__all__"
