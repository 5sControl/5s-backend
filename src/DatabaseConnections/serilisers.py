from rest_framework import serializers

from src.DatabaseConnections.models import ConnectionInfo


class ConnectionInfoSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)


class ConnectorStatusSerializer(serializers.Serializer):
    class Meta:
        model = ConnectionInfo
        fields = [
            "id",
            "type",
            "is_active",
        ]


class OdooItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
