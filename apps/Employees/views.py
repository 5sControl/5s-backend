from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from apps.Employees.forms import ContactForm
from apps.Employees.models import CustomUser, History, ImageUsers
from django.contrib.auth.models import User
from apps.Employees.serializers import UserSerializer, HistorySerializer, EmployeeSerializer, ImageUsersSerializer
from django.views.generic.edit import FormView, CreateView


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


class ImageViewSet(ModelViewSet):
    """List of all image"""
    serializer_class = ImageUsersSerializer
    queryset = ImageUsers.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class ContactView(CreateView):
    model = CustomUser
    form_class = ContactForm
    template_name = 'contact_form.html'
    success_url = '?success'