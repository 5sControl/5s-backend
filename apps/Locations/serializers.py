from rest_framework import serializers
from .models import Cameras, Gate, Location


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameras
        fields = ['name', 'id']


class GateSerializer(serializers.ModelSerializer):
    camera_input = CameraSerializer(many=False)
    camera_output = CameraSerializer(many=False)

    class Meta:
        model = Gate
        fields = ['name', 'id', 'camera_input', 'camera_output']


class LocationSerializer(serializers.ModelSerializer):
    gate_id = GateSerializer(many=False)

    class Meta:
        model = Location
        fields = ['name', 'id', 'gate_id']
