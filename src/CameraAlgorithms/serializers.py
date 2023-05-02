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
            "is_active",
        )


class CameraSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
    name = serializers.CharField(required=False)
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        ref_name = "camera-serializer"


class CameraProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        ref_name = "camera-process-serializer"
        fields = ("id", "name")


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        ref_name = "algo-serializer"


class AlgorithmStatusSerializer(serializers.Serializer):
    true = AlgorithmSerializer(many=True)
    false = AlgorithmSerializer(many=True)

    class Meta:
        ref_name = "algo-status"


class CameraAlgoritmsSerializer(serializers.Serializer):
    camera = CameraSerializer()
    algorithms = AlgorithmSerializer(many=True)

    class Meta:
        ref_name = "camera-algo"


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
        fields = ["camera", "algorithm", "process_id", "is_active"]


class CameraAlgorithmLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAlgorithmLog
        ref_name = "camera-algo-logs"
        fields = "__all__"
