from rest_framework import serializers

from src.Employees.models import CustomUser
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "date_joined", "role", "workplace"]
        read_only_fields = ["date_joined"]

    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField()
