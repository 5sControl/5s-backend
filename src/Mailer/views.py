from rest_framework import generics
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SMTPSettings, Emails
from django.core.mail import send_mail
from .serializers import SMTPSettingsSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Messages, Recipients
from .serializers import MessagesSerializer, RecipientsSerializer

# class EmailView(APIView):
#     def post(self, request, format=None):
#         subject = request.data.get('subject')
#         message = request.data.get('message')
#         recipient_list = request.data.get('recipient_list')
#         from_email = request.data.get('from_email', settings.DEFAULT_FROM_EMAIL)
#         fail_silently = request.data.get('fail_silently', False)
#
#         send_mail(
#             subject,
#             message,
#             from_email,
#             recipient_list,
#             fail_silently=fail_silently,
#         )
#
#         return Response({'detail': 'Email sent successfully.'})


class SMTPSettingsListCreateView(generics.ListCreateAPIView):
    queryset = SMTPSettings.objects.all().order_by('id')
    serializer_class = SMTPSettingsSerializer


class SMTPSettingsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SMTPSettings.objects.all().order_by('id')
    serializer_class = SMTPSettingsSerializer


class MessagesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Messages.objects.all().order_by('id')
    serializer_class = MessagesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            recipients_data = request.data.get('recipients', [])
            message = serializer.save()
            recipients = []
            for recipient in recipients_data:
                email_data = recipient.pop('email')
                email, created = Emails.objects.get_or_create(email=email_data)
                recipient['email'] = email.id
                recipient_serializer = RecipientsSerializer(data=recipient)
                if recipient_serializer.is_valid():
                    recipient_serializer.save(message=message)
                    recipients.append(recipient_serializer.data)
            response_data = serializer.data.copy()
            response_data['recipients'] = recipients
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagesDetailAPIView(generics.RetrieveAPIView):
    queryset = Messages.objects.all().order_by('id')
    serializer_class = MessagesSerializer


class RecipientsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Recipients.objects.all().order_by('id')
    serializer_class = RecipientsSerializer


class RecipientsDetailAPIView(generics.RetrieveAPIView):
    queryset = Recipients.objects.all().order_by('id')
    serializer_class = RecipientsSerializer
