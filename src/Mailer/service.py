from django.core.mail import send_mail

from datetime import datetime, time

from src.Mailer.models import SMTPSettings, WorkingTime, Emails
from django.core.mail.backends.smtp import EmailBackend


def send_email(item):

    work_time = WorkingTime.objects.last()
    email_list = Emails.objects.filter(is_active=True).values('email')
    subject = '5sControl notifications'
    message = f'Оповещение о минимальном уровне Item с именем {item.name}, на данный момент остаток составляет {item.current_stock_level}'
    recipient_list = []
    for email in email_list:
        recipient_list.append(email.get('email'))

    # email service check
    try:
        smtp_settings = SMTPSettings.objects.first()
    except SMTPSettings.DoesNotExist:
        raise Exception('SMTP configuration is not defined')

    # Check if a message was already
    today = datetime.now().time()
    start_time = work_time.time_start
    end_time = work_time.time_end

    if start_time < today < end_time:
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
