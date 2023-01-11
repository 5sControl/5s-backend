from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from apps.Employees.forms import ContactForm
from apps.Employees.models import CustomUser, History
from django.contrib.auth.models import User
from apps.Employees.serializers import EmployeeSerializer, HistorySerializer
from apps.Employees.serializers import UserSerializer, PeopleLocationsSerializers
from django.views.generic.edit import CreateView
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.generic import ListView

class UsersViewSet(ModelViewSet):
    """List of all users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class HomePageView(ListView):
    model = CustomUser
    template_name = "home.html"


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


class PeopleViewSet(viewsets.ViewSet):
    """List of all history and people"""
    def list(self, request):
        local = History.objects.all().values('location_id').union(History.objects.all().values_list('location_id'))
        users = History.objects.all().filter(people__status=True).values('people_id').distinct()
        qr = []
        for loc in local:
            locate = History.objects.all().filter(location_id=loc['location_id']).values('location__name').distinct()
            if locate not in qr:
                qr.append(locate[0])
        for user in users:
            qr.append((History.objects.filter(people_id=user['people_id'])
                       .values('people_id', 'people__first_name', 'people__last_name').distinct())[0])
        return Response(qr)
