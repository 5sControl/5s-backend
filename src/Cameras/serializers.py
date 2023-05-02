from rest_framework import serializers
from .models import Camera


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = [
            "id",
            "name",
            "username",
            "password",
            "is_active",
        ]


class CameraProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("id", "name")
