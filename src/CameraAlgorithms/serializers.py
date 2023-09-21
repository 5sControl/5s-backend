from rest_framework import serializers

from .models import Camera, ZoneCameras
from src.CameraAlgorithms.models import Algorithm, CameraAlgorithm, CameraAlgorithmLog


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


class ZoneIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class CreateConfigSerializer(serializers.Serializer):
    operation_control_id = serializers.CharField(required=False)
    zonesID = ZoneIdSerializer(many=True, required=False)


class CreateAlgorithmSerializer(serializers.Serializer):
    name = serializers.CharField()
    config = CreateConfigSerializer(required=False)


class CreateCameraAlgorithmSerializer(serializers.Serializer):
    camera = CreateCameraSerializer()
    algorithms = CreateAlgorithmSerializer(many=True, required=False)


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


class UniqueImageNameSerializer(serializers.Serializer):
    unique_image_names = serializers.SerializerMethodField()

    def get_unique_image_names(self, obj):
        algorithms = Algorithm.objects.exclude(image_name=None).values_list('image_name', flat=True).distinct()
        return algorithms

