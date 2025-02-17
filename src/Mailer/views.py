from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

import json


from src.Mailer.models import SMTPSettings, Emails, WorkingTime
from src.Mailer.serializers import SMTPSettingsSerializer, WorkingTimeSerializer, EmailsSerializer
from rest_framework import generics


class SMTPSettingsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = SMTPSettingsSerializer

    def get_queryset(self):
        return SMTPSettings.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No SMTP settings found."}, status=status.HTTP_404_NOT_FOUND)
        latest_setting = queryset.first()
        serializer = self.get_serializer(latest_setting)
        return Response(serializer.data)


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


def email_list(request):
    active_emails = Emails.objects.filter(is_active=True)
    email_list = [email.email for email in active_emails]
    emails_json = json.dumps(email_list)
    return HttpResponse(emails_json, content_type='application/json')


class WorkingTimeView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = WorkingTimeSerializer

    def get_queryset(self):
        last_working_time = WorkingTime.objects.last()
        if last_working_time is not None:
            return WorkingTime.objects.filter(id=last_working_time.id)
        return WorkingTime.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

