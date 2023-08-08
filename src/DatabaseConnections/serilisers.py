from rest_framework import serializers


class ConnectionInfoSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
