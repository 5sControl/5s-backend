from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from apps.Employees.forms import ContactForm
from apps.Employees.models import CustomUser, History
from django.contrib.auth.models import User
from apps.Employees.serializers import EmployeeSerializer, HistorySerializer
from apps.Employees.serializers import UserSerializer, PeopleLocationsSerializers
from django.views.generic.edit import CreateView




class UsersViewSet(ModelViewSet):
    """List of all users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
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


class ContactView(CreateView):
    model = CustomUser
    form_class = ContactForm
    template_name = 'contact_form.html'
    success_url = '?success'


class PeopleViewSet(ModelViewSet):
    """List of all history and people"""
    serializer_class = PeopleLocationsSerializers
    queryset = History.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]

