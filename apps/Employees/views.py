from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from apps.Employees.models import CustomUser, History
from apps.Employees.serializers import UserSerializer, HistorySerializer, EmployeeSerializer


class UsersViewSet(ModelViewSet):
    """List of all users"""
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class HistoryViewSet(ModelViewSet):
    """List of all history"""
    serializer_class = HistorySerializer
    queryset = History.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class EmployeeViewSet(ModelViewSet):
    """List of all employee"""
    serializer_class = EmployeeSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
