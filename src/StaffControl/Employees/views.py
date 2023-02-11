import os
import requests

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from src.StaffControl.Employees.serializers import (
    EmployeeSerializer,
    PeopleLocationsSerializers,
)
from src.StaffControl.Employees.serializers import UserSerializer

from src.StaffControl.Employees.models import CustomUser


class UsersViewSet(ModelViewSet):
    """List of all users"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class EmployeeViewSet(ModelViewSet):
    """List of all employee"""

    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = CustomUser.objects.all()
    http_method_names = [
        "get",
        "post",
        "delete",
        "put",
    ]

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        try:
            os.remove(f"database/dataset/encoding_{instance.id}.pickle")
        except Exception as exc:
            print(exc)
        finally:
            try:
                response = requests.post(
                    "http://face_recognition_queue:8008/api/update-dataasets/",
                    {"update_date": True},
                )
            except Exception as ex:
                print(ex)

            return super(EmployeeViewSet, self).destroy(request, pk, *args, **kwargs)


class PeopleViewSet(ReadOnlyModelViewSet):
    """List of all history and people"""

    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PeopleLocationsSerializers

    def list(self, *args, **kwargs):
        locations = []
        users_by_locations = {}

        user_info = CustomUser.objects.all()
        for location in user_info:
            if location.location != None:
                locations.append(str(location.location))
            else:
                locations.append(location.location)
        print(f"[INFO] {locations}")

        for location in locations:
            users_by_locations[location] = list(
                (
                    CustomUser.objects.filter(location__name=location).values_list(
                        "first_name", "last_name", "date_joined"
                    )
                )
            )
        print(f"[INFO] {users_by_locations}")

        return Response(users_by_locations)
