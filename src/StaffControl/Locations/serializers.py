from rest_framework import serializers
from .models import Gate, Location


class GateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gate
        fields = ["name", "id", "camera_input", "camera_output"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["name", "id", "gate_id"]
