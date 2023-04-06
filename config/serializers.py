from rest_framework import serializers


class CameraListSerializer(serializers.ListSerializer):
    result = serializers.ListField(child=serializers.IPAddressField())
