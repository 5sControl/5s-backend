from rest_framework import serializers

from src.Algorithms.models import CameraAlgorithm
from .models import Algorithm


class AlgorithmUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ["id", "is_available", "cameras"]


class CameraAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAlgorithm
        fields = ["id", "algorithm", "camera_id"]
