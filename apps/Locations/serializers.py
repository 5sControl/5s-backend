from rest_framework import serializers
from .models import Camera, Gate, Location


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ["id"]


class GateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gate
        fields = ["name", "id", "camera_input", "camera_output"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["name", "id", "gate_id"]
