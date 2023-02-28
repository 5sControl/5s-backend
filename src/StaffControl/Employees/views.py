import os
import requests

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from src.StaffControl.Employees.user_manager import UserManager

from src.core.permissions import IsStaffPermission, IsSuperuserPermission

from django.contrib.auth.models import User

from src.StaffControl.Employees.serializers import (
    EmployeeSerializer,
    PeopleLocationsSerializers,
    UserSerializer
)

from src.StaffControl.Employees.models import StaffControlUser


class UsersViewSet(ModelViewSet):
    """List of all users"""

    permission_classes = [IsAuthenticated, IsSuperuserPermission | IsStaffPermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class EmployeeViewSet(ModelViewSet):
    """List of all employee"""

    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = StaffControlUser.objects.all()
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

    queryset = StaffControlUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PeopleLocationsSerializers

    def list(self, *args, **kwargs):
        locations = []
        users_by_locations = {}

        user_info = StaffControlUser.objects.all()
        for location in user_info:
            if location.location != None:
                locations.append(str(location.location))
            else:
                locations.append(location.location)
        print(f"[INFO] {locations}")

        for location in locations:
            users_by_locations[location] = list(
                (
                    StaffControlUser.objects.filter(location__name=location).values_list(
                        "first_name", "last_name", "date_joined"
                    )
                )
            )
        print(f"[INFO] {users_by_locations}")

        return Response(users_by_locations)


class CreateUserView(generics.GenericAPIView):
    """Create new staff or worker user"""

    permission_classes = [IsAuthenticated, IsSuperuserPermission]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_type = request.data.get('user_type')
        username = request.data.get('username')
        password = request.data.get('password')

        if not user_type or not username or not password:
            return Response({'error': 'user_type, username, and password are required'})

        user_manager = UserManager()

        if user_type == 'staff':
            user_manager.create_staff(username, password)
        elif user_type == 'worker':
            user_manager.create_worker(username, password)
        else:
            return Response({'error': 'user_type must be "staff" or "worker"'}, status=400)

        return Response({'success': f'{user_type} user created successfully'})