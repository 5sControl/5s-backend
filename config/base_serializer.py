from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """Registers a employee"""

    class Meta:
        model = User
        ref_name = "UserSerializer"
        fields = ["username", "id", "date_joined", "password"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        print("YA UPDATE")
        return super(UserSerializer, self).update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    """ "A register serializer that can be used to register new administrators"""

    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    repeat_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        ref_name = "register user serializer"
        fields = [
            "username",
            "password",
            "repeat_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        repeat_password = validated_data["repeat_password"]
        if password != repeat_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
