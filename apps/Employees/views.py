from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from apps.Employees.forms import ContactForm
from apps.Employees.models import CustomUser, History
from django.contrib.auth.models import User
from apps.Employees.serializers import UserSerializer, EmployeeSerializer, HistorySerializer
from apps.Employees.serializers import UserSerializer
from django.views.generic.edit import CreateView

from apps.Locations.models import Location


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


class PeopleViewSet(ModelViewSet):
    """List of all history and people"""
    serializer_class = HistorySerializer
    data = History.objects.all().values()
    # print(data)
    location = Location.objects.filter(id=data[0]['location_id']).values('name')[0]['name']
    people = CustomUser.objects.filter(id=data[0]['people_id']).values().filter(status=True)
    # print('people=', people)
    # queryset = History.objects.all().values()
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