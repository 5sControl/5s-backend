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
        image = ImageUsersSerializer(many=True)

        def create(self, validated_data):
            images_data = validated_data.pop('image')
            image = CustomUser.objects.create(**validated_data)
            for image_data in images_data:
                ImageUsers.objects.create(image=image, **image_data)
            return image

        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'dataset', 'date_joined', 'image']


class HistorySerializer(serializers.ModelSerializer):
    people = EmployeeSerializer(many=True)
    location = LocationSerializer(many=True)

    class Meta:
        model = History
        fields = ['people', 'id', 'location', 'entry_date', 'release_date', 'image']

    # def create(self, validated_data):
    #     images_data = validated_data.pop('location')
    #     album = History.objects.create(**validated_data)
    #     for image_data in images_data:
    #         Location.objects.create(album=album, *image_data)
    #     for image_data in images_data:
    #         CustomUser.objects.create(album=album, *image_data)
    #     return album

