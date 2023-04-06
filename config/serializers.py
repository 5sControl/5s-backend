from rest_framework import serializers


class CameraListSerializer(serializers.ListSerializer):
    child = serializers.CharField()

    def to_representation(self, data):
        return data
