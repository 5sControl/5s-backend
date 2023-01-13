from rest_framework.viewsets import ModelViewSet

from rest_framework import viewsets, permissions, response

from django.contrib.auth.models import User

from apps.Employees.serializers import EmployeeSerializer, PeopleLocationsSerializers
from apps.Employees.serializers import UserSerializer

from apps.Employees.models import CustomUser
from apps.base.permissions import IsAdminOrReadOnly


class UsersViewSet(ModelViewSet):
    """List of all users"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,
    # ]


class EmployeeViewSet(ModelViewSet):
    """List of all employee"""

    serializer_class = EmployeeSerializer
    queryset = CustomUser.objects.all()

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,
    # ]


class PeopleViewSet(viewsets.ReadOnlyModelViewSet):
    """List of all history and people"""

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,
    # ]
    serializer_class = PeopleLocationsSerializers

    def list(self, request, *args, **kwargs):
        locations = []
        users_by_locations = {}

        user_info = CustomUser.objects.all()
        for location in user_info:
            if location.location != None:
                locations.append(str(location.location))
            else:
                locations.append(location.location)
        print(f'[INFO] {locations}')

        for location in locations:
            users_by_locations[location] = list((CustomUser.objects
                                                 .filter(location__name=location)
                                                 .values_list(
                                                     'first_name', 'last_name', 'date_joined')))
        print(f'[INFO] {users_by_locations}')

        return response.Response(users_by_locations)