from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from src.Mailer.decorators import send_email_within_hours

from datetime import datetime, time

from django.utils import timezone

from src.Mailer.models import SMTPSettings, Recipients, NotificationsSent
from django.core.mail.backends.smtp import EmailBackend


# @send_email_within_hours(time(9, 0), time(18, 0))
def send_email(item):
    recipient = Recipients.objects.filter(item_id=item.id).values('email__email', 'message__message', 'message__subject')
    subject = recipient[0].get('message__subject')
    message = recipient[0].get('message__message')
    recipient_list = [d.get('email__email') for d in recipient]

    # email service check
    try:
        smtp_settings = SMTPSettings.objects.first()
    except SMTPSettings.DoesNotExist:
        raise Exception('SMTP configuration is not defined')

    # Check if a message was already sent today
    today = timezone.now().date()
    # sent_today = Messages.objects.filter(date_created__date=today, is_send=True).exists()
    # if sent_today:
    #     return Response({'detail': 'A message has already been sent today'}, status=status.HTTP_400_BAD_REQUEST)

    # sending email
    connection = EmailBackend(
        host=smtp_settings.server,
        port=smtp_settings.port,
        username=smtp_settings.username,
        password=smtp_settings.password,
        use_tls=smtp_settings.email_use_tls,
        use_ssl=smtp_settings.email_use_ssl,
    )
    send_mail(
        subject,
        message,
        smtp_settings.username,
        recipient_list,
        fail_silently=False,
        connection=connection,
    )

    # return Response({'success': True})
