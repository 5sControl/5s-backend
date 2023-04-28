from rest_framework import serializers

from src.MsSqlConnector.models import DatabaseConnection

from src.OrderView.models import IndexOperations


class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ["id", "database_type", "server", "database", "username", "password" "port"]


class ProductSerializer(serializers.Serializer):
    indeks = serializers.IntegerField()
    zlecenie = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255)
    terminrealizacji = serializers.DateTimeField()
    datawejscia = serializers.DateTimeField()


class IndexStanowiskoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexOperations
        fields = [
            "id",
            "type_operation",
            "camera",
        ]
