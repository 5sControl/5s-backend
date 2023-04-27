from rest_framework import serializers
from .models import Camera


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = (
            "id",
            "name",
            "username",
            "description",
            "is_active",
        )


class CameraProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("id", "name")


class CreateCameraSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
    username = serializers.CharField()
    password = serializers.CharField()


class UpdateCameraSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
    username = serializers.CharField()
    description = serializers.CharField()
