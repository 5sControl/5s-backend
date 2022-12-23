from rest_framework import serializers
from .models import Cameras, Gate, Location
from django.contrib.auth.hashers import make_password


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameras
        fields = ['name', 'id']


class GateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gate
        fields = ['name', 'id', 'camera_input', 'camera_output']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'id', 'people_id', 'gate_id']
