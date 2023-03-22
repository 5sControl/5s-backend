from rest_framework import serializers

from src.OrderView.models import DatabaseConnection


class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ["id", "database_type", "server", "database", "username"]
