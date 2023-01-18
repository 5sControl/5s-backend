import datetime
import pickle
from rest_framework import serializers
from .models import CustomUser
from .recognitions import Recognition
from ..Locations.models import Location
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """Registers a employee"""

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
    """"A register serializer that can be used to register new administrators"""

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
    """Create a Employee with his dataset."""

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'dataset', 'date_joined', 'image1', 'image2', 'image3',
                  'image4', 'image5', 'location', 'status']

    def create(self, validated_data):
        data = Recognition().dataset_maker(validated_data=validated_data)
        if data == None:
            raise serializers.ValidationError
        user = CustomUser.objects.create(**validated_data)

        with open(f'database/dataset/encoding_{user.id}.pickle', 'wb') as file:
            file.write(pickle.dumps(data))

        dataset = f'database/dataset/encoding_{user.id}.pickle'
        user.dataset = dataset
        user.save()
        return user


class PeopleLocationsSerializers(serializers.ModelSerializer):
    """Displays information of all employees in a given location"""

    class Meta:
        model = CustomUser
        exclude = ('image', )
