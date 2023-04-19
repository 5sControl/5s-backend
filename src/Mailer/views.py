from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.Mailer.models import SMTPSettings, Emails, WorkingTime
from src.Mailer.serializers import SMTPSettingsSerializer, WorkingTimeSerializer, EmailsSerializer
from rest_framework import generics


class SMTPSettingsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = SMTPSettings.objects.all().order_by('id')
    serializer_class = SMTPSettingsSerializer


class SMTPSettingsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = SMTPSettings.objects.all().order_by('id')
    serializer_class = SMTPSettingsSerializer


class EmailsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = Emails.objects.all().order_by('id')
    serializer_class = EmailsSerializer


class WorkingTimeView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = WorkingTime.objects.all().order_by('id')
    serializer_class = WorkingTimeSerializer
