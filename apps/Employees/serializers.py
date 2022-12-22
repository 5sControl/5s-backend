from rest_framework import serializers
from .models import Employee
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['username', 'email', 'id', 'first_name', 'last_name', 'date_joined', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        print('YA UPDATE')
        return super(UserSerializer, self).update(instance, validated_data)

