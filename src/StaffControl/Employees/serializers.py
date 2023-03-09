# import os
# import pickle
# import requests

# from rest_framework import serializers
# from .models import StaffControlUser
# # from .recognitions import Recognition, face_rec
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password


# class UserSerializer(serializers.ModelSerializer):
#     """Registers a employee"""

#     class Meta:
#         model = User
#         ref_name = "UserSerializer"
#         fields = ["username", "id", "date_joined", "password"]

#     def create(self, validated_data):
#         validated_data["password"] = make_password(validated_data["password"])
#         return super(UserSerializer, self).create(validated_data)

#     def update(self, instance, validated_data):
#         validated_data["password"] = make_password(validated_data["password"])
#         print("YA UPDATE")
#         return super(UserSerializer, self).update(instance, validated_data)


# class RegisterSerializer(serializers.ModelSerializer):
#     """ "A register serializer that can be used to register new administrators"""

#     password = serializers.CharField(write_only=True, style={"input_type": "password"})
#     repeat_password = serializers.CharField(
#         write_only=True, style={"input_type": "password"}
#     )

#     class Meta:
#         model = User
#         ref_name = "register user serializer"
#         fields = [
#             "username",
#             "password",
#             "repeat_password",
#         ]
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         username = validated_data["username"]
#         password = validated_data["password"]
#         repeat_password = validated_data["repeat_password"]
#         if password != repeat_password:
#             raise serializers.ValidationError({"password": "Passwords do not match"})
#         user = User(username=username)
#         user.set_password(password)
#         user.save()
#         return user


# class EmployeeSerializer(serializers.ModelSerializer):
#     """Create a Employee with his dataset."""

#     class Meta:
#         model = StaffControlUser
#         fields = [
#             "id",
#             "first_name",
#             "last_name",
#             "dataset",
#             "date_joined",
#             "image_below",
#             "image_above",
#             "image_center",
#             "image_left",
#             "image_right",
#             "location",
#             "status",
#         ]

#     def create(self, validated_data):
#         user = StaffControlUser.objects.create(**validated_data)

#         data = Recognition().dataset_maker(validated_data=validated_data)
#         if len(data) == 0:
#             user.delete()
#             raise serializers.ValidationError

#         with open(f"database/dataset/encoding_{user.id}.pickle", "wb") as file:
#             file.write(pickle.dumps(data))

#         dataset = f"database/dataset/encoding_{user.id}.pickle"
#         user.dataset = dataset
#         user.save()
#         face_rec(validated_data)

#         try:
#             response = requests.post(
#                 "http://face_recognition_queue:8008/api/update-dataasets/",
#                 {"update_date": True},
#             )
#         except Exception as ex:
#             print(ex)

#         return user

#     def update(self, instance, validated_data):
#         instance.last_name = validated_data["last_name"]
#         instance.first_name = validated_data["first_name"]
#         instance.image_below = validated_data["image_below"]
#         instance.image_above = validated_data["image_above"]
#         instance.image_center = validated_data["image_center"]
#         instance.image_left = validated_data["image_left"]
#         instance.image_right = validated_data["image_right"]
#         instance.status = validated_data["status"]
#         instance.dataset = validated_data["dataset"]
#         instance.location = validated_data["location"]
#         instance.save()

#         data = Recognition().dataset_maker(validated_data=validated_data)
#         if len(data) == 0:
#             instance.delete()
#             raise serializers.ValidationError
#         try:
#             os.remove(f"database/dataset/encoding_{instance.id}.pickle")
#         except Exception as exc:
#             print(exc)

#         with open(f"database/dataset/encoding_{instance.id}.pickle", "wb") as file:
#             file.write(pickle.dumps(data))

#         face_rec(validated_data)

#         try:
#             response = requests.post(
#                 "http://face_recognition_queue:8008/api/update-dataasets/",
#                 {"update_date": True},
#             )
#         except Exception as ex:
#             print(ex)

#         return instance


# class PeopleLocationsSerializers(serializers.ModelSerializer):
#     """Displays information of all employees in a given location"""

#     class Meta:
#         model = StaffControlUser
#         exclude = (
#             "date_joined",
#             "image_below",
#             "image_above",
#             "image_center",
#             "image_left",
#             "image_right",
#         )
