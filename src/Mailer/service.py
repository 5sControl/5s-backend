from django.core.mail import send_mail

from datetime import datetime, time

from src.Mailer.models import SMTPSettings, Recipients, NotificationsSent
from django.core.mail.backends.smtp import EmailBackend


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
    today = datetime.now().date()
    start_time = time(9, 0, 0)
    end_time = time(18, 0, 0)
    sent_today = NotificationsSent.objects.filter(
        recipients__item_id=item.id,
        date_created__date=today,
        date_created__time__range=(start_time, end_time)
    ).exists()
    if not sent_today:

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

        # Save the record of sent notifications
        recipients = Recipients.objects.filter(item_id=item.id)
        for recipient in recipients:
            NotificationsSent.objects.create(recipients=recipient)

    # return Response({'success': True})
