from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from apps.Employees.models import Employee
from apps.Employees.serializers import UserSerializer


class UsersViewSet(ModelViewSet):
    """List of all users"""
    serializer_class = UserSerializer
    queryset = Employee.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
