import pickle
from rest_framework import serializers, response
from .models import CustomUser, History
from .recognitions import Recognition
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ..Locations.models import Location
from ..Locations.serializers import LocationSerializer, CameraSerializer
import face_recognition


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
        fields = ['id', 'first_name', 'last_name', 'dataset', 'date_joined', 'image', 'status']

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        data = Recognition().dataset_maker(validated_data=validated_data)

        with open(f'database/dataset/encoding_{user.id}.pickle', 'wb') as file:
            file.write(pickle.dumps(data))

        dataset = f'database/dataset/encoding_{user.id}.pickle'
        user.dataset = dataset
        user.save()
        return user


class HistorySerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        if validated_data['action']:
            image = validated_data['image']
            camera = validated_data['camera']
            action = validated_data['action']
            name_file = validated_data['name_file']
            id_people = int(((f"[{validated_data['name_file']}").split('_')[-1]).split('.')[0])
            location = Location.objects.filter(gate_id__camera_input__id=validated_data['camera'])[0]
            history_data = History(
                camera=camera,
                action=action,
                name_file=name_file,
                location=location,
                people=CustomUser.objects.get(id=id_people),
                image=image
            )
            history_data.save()
            user = CustomUser.objects.filter(id=id_people)
            user.update(status=True)


        return history_data

    class Meta:
        model = History
        fields = ['id', 'people', 'location', 'image', 'entry_date', 'release_date', 'camera', 'name_file', 'action']
        read_only_fields = ['entry_date']


class PeopleLocationsSerializers(serializers.ModelSerializer):
    people = EmployeeSerializer(many=False)
    location = LocationSerializer(many=False)

    class Meta:
        model = History
        fields = ['id', 'location', 'people']
