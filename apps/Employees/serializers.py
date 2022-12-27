from rest_framework import serializers
from .models import CustomUser, History
from apps.Locations.serializers import LocationSerializer
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'id', 'first_name', 'last_name', 'date_joined', 'password', 'dataset', 'location']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        print('YA UPDATE')
        return super(UserSerializer, self).update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})
    repeat_password = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
            'repeat_password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        repeat_password = validated_data['repeat_password']
        if password != repeat_password:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})
        user = CustomUser(username=username)
        user.set_password(password)
        user.save()
        return user


class HistorySerializer(serializers.ModelSerializer):
    people = UserSerializer(many=False)

    class Meta:
        model = History
        fields = ['people', 'id', 'entry_date', 'release_date', 'image']


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'dataset', 'date_joined']
