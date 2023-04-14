from rest_framework.viewsets import ModelViewSet

from src.Mailer.models import SMTPSettings, Emails, WorkingTime
from src.Mailer.serializers import SMTPSettingsSerializer, WorkingTimeSerializer, EmailsSerializer
from rest_framework import generics


class SMTPSettingsListCreateView(generics.ListCreateAPIView):
    queryset = SMTPSettings.objects.all().order_by('id')
    serializer_class = SMTPSettingsSerializer


class SMTPSettingsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SMTPSettings.objects.all().order_by('id')
    serializer_class = SMTPSettingsSerializer


class EmailsView(ModelViewSet):
    queryset = Emails.objects.all().order_by('id')
    serializer_class = EmailsSerializer


class WorkingTimeView(ModelViewSet):
    queryset = WorkingTime.objects.all().order_by('id')
    serializer_class = WorkingTimeSerializer
