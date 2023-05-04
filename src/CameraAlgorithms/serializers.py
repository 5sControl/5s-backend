from rest_framework import serializers
from src.Algorithms.models import Algorithm, CameraAlgorithm, CameraAlgorithmLog

from src.Cameras.models import Camera


class CameraModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        ref_name = "camera-model-serializer"
        fields = (
            "id",
            "name",
            "username",
            "password",
            "is_active",
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

    class Meta:
        ref_name = "camera-algo"


class CameraProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        ref_name = "camera-process-serializer"
        fields = ("id", "name")


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ("id", "name")
        ref_name = "algo-serializer"


class AlgorithmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = "__all__"
        ref_name = "algo-serializer"


class StopAlgorithmSerializer(serializers.Serializer):
    pid = serializers.IntegerField()

    class Meta:
        ref_name = "stop-algo"


class UpdateCameraSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
    username = serializers.CharField()

    class Meta:
        ref_name = "update-camera"


class CameraAlgorithmFullSerializer(serializers.ModelSerializer):
    algorithm = AlgorithmSerializer()
    camera = CameraProcessSerializer()

    class Meta:
        model = CameraAlgorithm
        ref_name = "camera-algor-full"
        fields = [
            "camera",
            "algorithm",
            "process_id",
            "is_active"
        ]


class CameraAlgorithmLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAlgorithmLog
        ref_name = "camera-algo-logs"
        fields = "__all__"
