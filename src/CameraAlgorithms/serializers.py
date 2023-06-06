from rest_framework import serializers

from .models import Camera, ZoneCameras
from .models import Algorithm, CameraAlgorithm, CameraAlgorithmLog


class CameraModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = (
            "id",
            "name",
            "username",
            "password",
            "is_active",
        )


class CameraReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = (
            "id",
            "name",
            "username",
        )


class CreateCameraSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
    name = serializers.CharField(required=False)
    username = serializers.CharField()
    password = serializers.CharField()


class CreateConfigSerializer(serializers.Serializer):
    operation_control_id = serializers.CharField()


class CreateAlgorithmSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = CreateConfigSerializer(required=False)


class CreateCameraAlgorithmSerializer(serializers.Serializer):
    camera = CreateCameraSerializer()
    algorithms = CreateAlgorithmSerializer(many=True)


class CameraProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("id", "name")


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ("id", "name")


class AlgorithmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = "__all__"


class StopAlgorithmSerializer(serializers.Serializer):
    pid = serializers.IntegerField()


class UpdateCameraSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
    username = serializers.CharField()


class CameraAlgorithmFullSerializer(serializers.ModelSerializer):
    algorithm = AlgorithmSerializer()
    camera = CameraProcessSerializer()

    class Meta:
        model = CameraAlgorithm
        ref_name = "camera-algor-full"
        fields = ["camera", "algorithm", "process_id", "is_active"]


class CameraAlgorithmLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAlgorithmLog
        fields = "__all__"


class ZoneCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneCameras
        fields = "__all__"
        read_only_fields = ["is_active"]
