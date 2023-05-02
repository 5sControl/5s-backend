from rest_framework import serializers

from src.CameraAlgorithms.models.algorithm import CameraAlgorithm, CameraAlgorithmLog

from .models.camera import Camera


class CameraModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
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


class CameraProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("id", "name")


class AlgorithmSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = serializers.DictField()


class AlgorithmStatusSerializer(serializers.Serializer):
    true = AlgorithmSerializer(many=True)
    false = AlgorithmSerializer(many=True)


class CameraAlgoritmsSerializer(serializers.Serializer):
    camera = CameraSerializer()
    algorithms = AlgorithmSerializer(many=True)


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
        fields = ["camera", "algorithm", "process_id", "is_active"]


class CameraAlgorithmLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAlgorithmLog
        fields = "__all__"
