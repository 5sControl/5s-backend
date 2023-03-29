from rest_framework import generics
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SMTPSettings
from django.core.mail import send_mail
from .serializers import SMTPSettingsSerializer


class EmailView(APIView):
    def post(self, request, format=None):
        subject = request.data.get('subject')
        message = request.data.get('message')
        recipient_list = request.data.get('recipient_list')
        from_email = request.data.get('from_email', settings.DEFAULT_FROM_EMAIL)
        fail_silently = request.data.get('fail_silently', False)

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=fail_silently,
        )

        return Response({'detail': 'Email sent successfully.'})


class SMTPSettingsListCreateView(generics.ListCreateAPIView):
    queryset = SMTPSettings.objects.all()
    serializer_class = SMTPSettingsSerializer


class SMTPSettingsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SMTPSettings.objects.all()
    serializer_class = SMTPSettingsSerializer
