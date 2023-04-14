from rest_framework import generics
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SMTPSettings, Emails
from django.core.mail import send_mail
from .serializers import SMTPSettingsSerializer
from rest_framework import generics, status
from rest_framework.response import Response


class SMTPSettingsListCreateView(generics.ListCreateAPIView):
    queryset = SMTPSettings.objects.all().order_by('id')
    serializer_class = SMTPSettingsSerializer


class SMTPSettingsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SMTPSettings.objects.all().order_by('id')
    serializer_class = SMTPSettingsSerializer
