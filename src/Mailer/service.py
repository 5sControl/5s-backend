from django.core.mail import send_mail
from django.core.mail import EmailMessage

from datetime import datetime, time

from src.Mailer.models import SMTPSettings, WorkingTime, Emails
from django.core.mail.backends.smtp import EmailBackend


def send_email(item):
    work_time = WorkingTime.objects.last()
    email_list = Emails.objects.filter(is_active=True).values('email')
    subject = f'Low Stock Alert: {item.name}'
    message = f"Low Stock Alert: {item.name}\nThe inventory level of {item.name} in your stock has fallen to a low level. This means that there are only a limited number of units left in stock and that the item may soon become unavailable. The current quantity of {item.current_stock_level} is {item.low_stock_level}. To avoid any inconvenience, we recommend that you take action to replenish your stock of {item.name} as soon as possible."
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
        # create email message
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=smtp_settings.username,
            to=recipient_list
        )

        # attach image
        image_path = '../../images/76cb05d0-2a16-424b-ad5f-b9714a9a1365.jpg'
        with open(image_path, 'rb') as f:
            image_data = f.read()
        email_message.attach(filename=f'{item.image_item}', content=image_data, mimetype='images/jpg')

        # send email
        email_message.send(fail_silently=False, connection=connection)
