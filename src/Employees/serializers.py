from rest_framework import serializers

from src.Employees.models import CustomUser
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        ref_name = "user-ser"
        fields = [
            "id",
            "username",
            "date_joined",
            "status",
        ]

    date_joined = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%f %z", required=False)

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).update(instance, validated_data)

    def get_status(self, obj):
        if obj.is_superuser:
            return "superuser"
        elif obj.is_staff:
            return "admin"
        else:
            return "worker"


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField()
