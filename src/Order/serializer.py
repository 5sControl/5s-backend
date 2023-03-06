from rest_framework import serializers


class DatabaseConnectionSerializer(serializers.Serializer):
    db_name = serializers.CharField(required=True, max_length=255)
    db_user = serializers.CharField(required=True, max_length=255)
    db_password = serializers.CharField(required=True, max_length=255)
    db_port = serializers.CharField(required=True, max_length=255)
    db_host = serializers.CharField(required=True, max_length=255)