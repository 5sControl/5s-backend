from rest_framework import serializers
from .models import CustomUser, History, ImageUsers
from apps.Locations.models import Location
from apps.Locations.serializers import LocationSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class ImageUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUsers
        fields = ['id', 'image_user']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'id', 'date_joined', 'password']

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
        model = User
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
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'dataset', 'date_joined', 'image']

    def create(self, validated_data):
        all_images = (validated_data['image'])
        for image in all_images:
            print(image.image_user)
        return CustomUser.objects.create(**validated_data)


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = ['people', 'id', 'location', 'entry_date', 'release_date', 'image']
    

class CreateHistorySerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        location = validated_data['location']
        image = validated_data['image']
        

        location.save()
        return History.objects.create(**validated_data)

    class Meta:
        model = History
        fields = ['location', 'image']