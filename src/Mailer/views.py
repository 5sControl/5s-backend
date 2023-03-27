import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from rest_framework import generics
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SMTPSettings
from django.core.mail import send_mail
from .serializers import SMTPSettingsSerializer, EmailSerializer


class MailerViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_email = serializer.validated_data.get('to_email')
        subject = serializer.validated_data.get('subject')
        message = serializer.validated_data.get('message')

        send_mail(
            subject=subject,
            message=message,
            from_email='sender@example.com',
            recipient_list=[to_email],
            fail_silently=False,
        )

        return Response({'success': True})


class EmailView(APIView):
    def post(self, request):
        smtp_settings = SMTPSettings.objects.first()
        if not smtp_settings:
            return Response({'error': 'SMTP settings not found'}, status=500)
        from_email = request.data.get('from_email')
        to_emails = request.data.get('to_emails')
        cc_emails = request.data.get('cc_emails', [])
        bcc_emails = request.data.get('bcc_emails', [])
        subject = request.data.get('subject')
        body = request.data.get('body')
        attachments = request.data.get('attachments', [])
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_emails)
        msg['Cc'] = ', '.join(cc_emails)
        msg['Bcc'] = ', '.join(bcc_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(body))
        for attachment in attachments:
            file = MIMEApplication(attachment['content'], Name=attachment['filename'])
            file['Content-Disposition'] = f'attachment; filename="{attachment["filename"]}"'
            msg.attach(file)
        try:
            with smtplib.SMTP(smtp_settings.server, smtp_settings.port) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(smtp_settings.username, smtp_settings.password)
                smtp.send_message(msg)
            return Response({'success': 'Email sent'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SMTPSettingsListCreateView(generics.ListCreateAPIView):
    queryset = SMTPSettings.objects.all()
    serializer_class = SMTPSettingsSerializer


class SMTPSettingsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SMTPSettings.objects.all()
    serializer_class = SMTPSettingsSerializer
