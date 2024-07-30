from rest_framework import serializers

from src.DatabaseConnections.models import ConnectionInfo

from src.OrderView.models import IndexOperations


class ApiConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionInfo
        fields = [
            "id",
            "type",
            "is_active",
            "host",
        ]

    def create(self, validated_data):
        ConnectionInfo.objects.filter(type="api").delete()
        return super().create(validated_data)


class DatabaseConnectionSerializer(serializers.ModelSerializer):
    dbms = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = ConnectionInfo
        fields = [
            "id",
            "type",
            "dbms",
            "is_active",
            "server",
            "database",
            "username",
            "password",
            "port",
        ]

    def create(self, validated_data):
        ConnectionInfo.objects.filter(type="database").delete()
        return super().create(validated_data)


class ConnectionStatusSerializer(serializers.Serializer):
    db = DatabaseConnectionSerializer(read_only=True)
    api = ApiConnectionSerializer(read_only=True)


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


class ConnectionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionInfo
        fields = '__all__'


class DeleteConnectionSerializer(serializers.Serializer):
    pass


class OperationNameSerializer(serializers.Serializer):
    pass


class OrderDataByZlecenieSerializer(serializers.ListSerializer):
    pass
