from rest_framework.viewsets import ModelViewSet

from rest_framework import viewsets, permissions

from django.contrib.auth.models import User

from apps.Employees.serializers import EmployeeSerializer, HistorySerializer
from apps.Employees.serializers import UserSerializer

from apps.Employees.models import CustomUser, History
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
        ...