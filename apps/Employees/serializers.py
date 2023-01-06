from rest_framework import serializers, response

from .models import CustomUser, History
from .recognitions import Recognition

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from ..Locations.models import Location
from ..Locations.serializers import LocationSerializer

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
        dataset = Recognition().dataset_maker(validated_data=validated_data)
        user.dataset = dataset
        user.save()
        return user


class HistorySerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        face_img = face_recognition.load_image_file(f"{validated_data['image']}")
        if len(face_recognition.face_encodings(face_img)) > 0:

            dataset = face_recognition.face_encodings(face_img)[0]
            if CustomUser.objects.filter(dataset=(dataset)):

                #####################
                image = validated_data['image']
                location = Location.objects.get(id=1)
                history_data = History(
                    location=location,
                    people=CustomUser.objects.get(dataset=dataset),
                    image=image
                )
                history_data.save()
                #####################
                # location = validated_data['location']
                # print(type(location))
                # image = validated_data['image']
                # history_data = History.objects.create(location=location,
                #                                     people=CustomUser.objects.get(dataset=dataset), image=image)
                user = CustomUser.objects.filter(id=history_data.people.id)
                user.update(status=True)
                print(f"[INFO] history record successfully created with user {user}")
                return history_data
            else:

                print(validated_data)
                user = CustomUser.objects.create(**validated_data)
                user.dataset = dataset
                user.status = True
                user.save()

                #####################
                image = validated_data['image']
                location = Location.objects.get(id=1)
                history_data = History(
                    location=location,
                    people=CustomUser.objects.get(dataset=dataset),
                    image=image
                )
                history_data.save()
                #####################
                # location = validated_data['location']
                # image = validated_data['image']
                # history_data = History.objects.create(location=location, people=user.objects, image=image)

                print('Unrecognized user record successfully created')
                return history_data
        else:
            print('[ERROR] Face wasnt found')
            return response.Response(status=404)

    class Meta:
        model = History
        fields = ['id', 'people', 'location', 'image', 'release_date']
        read_only_fields = ['entry_date']


class PeopleLocationsSerializers(serializers.ModelSerializer):
    people = EmployeeSerializer(many=False)
    location = LocationSerializer(many=False)

    class Meta:
        model = History
        fields = ['location', 'people']
