from rest_framework import serializers


class CameraFinderSerializer(serializers.Serializer):
    ipaddress = serializers.CharField()
