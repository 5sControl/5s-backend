from rest_framework import serializers
from .models import CustomUser, History
import face_recognition
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


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
        face_img = face_recognition.load_image_file(f"media/photo/{validated_data['image']}")
        dataset = face_recognition.face_encodings(face_img)[0]
        user.dataset = dataset
        user.save()
        return user


class HistorySerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        face_img = face_recognition.load_image_file(f"media/photo/{validated_data['image']}")
        dataset = face_recognition.face_encodings(face_img)[0]

        if CustomUser.objects.filter(dataset=(dataset)):
            location = validated_data['location']
            image = validated_data['image']
            history_data = History.objects.create(location=location,
                                                  people=CustomUser.objects.get(dataset=dataset), image=image)
            user = CustomUser.objects.filter(id=history_data.people.id)
            user.update(status=True)
        else:
            # new user
            user = CustomUser.objects.create(**validated_data)
            user.dataset = dataset
            user.status = True
            user.save()

            # history record
            location = validated_data['location']
            image = validated_data['image']
            history_data = History.objects.create(location=location, people=user.objects, image=image)

        return history_data

    class Meta:
        model = History
        fields = ['people', 'location', 'image', 'release_date']
        read_only_fields = ['entry_date']
