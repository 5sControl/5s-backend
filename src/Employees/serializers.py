from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        ref_name = "user-ser"
        fields = [
            "id",
            "username",
            "date_joined",
            "status",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).update(instance, validated_data)

    def get_status(self, obj):
        if obj.is_superuser:
            return "owner"
        elif obj.is_staff:
            return "admin"
        else:
            return "worker"
