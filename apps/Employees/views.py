from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response

from rest_framework import viewsets, permissions

from django.contrib.auth.models import User

from apps.Employees.serializers import EmployeeSerializer, HistorySerializer
from apps.Employees.serializers import UserSerializer

from apps.Employees.models import CustomUser, History
from apps.Locations.models import Location
from apps.base.permissions import IsAdminOrReadOnly


class UsersViewSet(ModelViewSet):
    """List of all users"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [
            permissions.IsAuthenticatedOrReadOnly,
            IsAdminOrReadOnly,]


class HistoryViewSet(ModelViewSet):
    """List of all history"""

    serializer_class = HistorySerializer
    queryset = History.objects.all()

    permission_classes = [
            permissions.IsAuthenticatedOrReadOnly,
            IsAdminOrReadOnly,]


class EmployeeViewSet(ModelViewSet):
    """List of all employee"""
	
    serializer_class = EmployeeSerializer
    queryset = CustomUser.objects.all()

    permission_classes = [
            permissions.IsAuthenticatedOrReadOnly,
            IsAdminOrReadOnly,]


class PeopleViewSet(viewsets.ViewSet):
    """List of all history and people"""

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,]

    def list(self, request):
        local = History.objects.all().values('location_id').union(History.objects.all().values_list('location_id'))
        users = History.objects.all().filter(people__status=True).values('people_id').distinct()
        qr = []
        for loc in local:
            locate = History.objects.all().filter(location_id=loc['location_id']).values('location__name').distinct()
            if locate not in qr:
                loc = [(locate[0])]
                ds = []
                for user in users:
                    ds.append((History.objects.filter(people_id=user['people_id'])
                               .values('people_id', 'people__first_name', 'people__last_name').distinct())[0])
                loc.append(ds)
            qr.append(loc)
        return Response(Location.objects.all().values('name', 'gate_id'))