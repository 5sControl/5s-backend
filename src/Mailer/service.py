import os

import smtplib
from email.message import EmailMessage

from datetime import datetime
from src.Core.const import SERVER_URL

from src.Mailer.models import SMTPSettings, WorkingTime, Emails


def send_notification_email(item, count, image_path, item_status):
    work_time = WorkingTime.objects.last()
    email_list = Emails.objects.filter(is_active=True).values('email')
    subject = f'5S Control {item_status} Alert: {item.name}'
    if item_status == 'Low stock level':
        message = f'Current stock of {item.name}: {count}.\nLow stock level of {item.name}: {item.low_stock_level}.\nThe inventory level of {item.name} in your stock has fallen to a low level. This means that there are only a limited number of units left in stock and that the item may soon become unavailable.\nTo avoid any inconvenience, we recommend that you take action to replenish your stock of {item.name} as soon as possible.\n\n{SERVER_URL}:3000/inventory\n\nYou are receiving this email because your email account was entered in 5S Control system to receive notifications regarding low stock levels of inventory.'
    elif item_status == 'Out of stock':
        message = f'{item.name} is currently out of stock. \nTo avoid any inconvenience, we recommend that you take ' \
                  f'action to replenish your stock of {item.name} as soon as pos' \
                  f'sible.\n\n{SERVER_URL}:3000/inventory\n\nYou are receiving this email because your email account ' \
                  f'was entered in 5S Control system to receive notifications regarding low stock levels of inventory.'

    image_name = image_path.split('/')[-1]

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

        with smtplib.SMTP_SSL(smtp_settings.server, smtp_settings.port) as smtp:
            smtp.login(smtp_settings.username, smtp_settings.password)

            email_message = EmailMessage()
            email_message['Subject'] = subject
            email_message['From'] = smtp_settings.username
            email_message['To'] = recipient_list
            email_message.set_content(message)

            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', f'{image_path}')
            with open(image_path, 'rb') as f:
                image_data = f.read()
            email_message.add_attachment(image_data, maintype='image', subtype='jpg', filename=image_name)

            smtp.send_message(email_message)

    else:
        print('Working time limit, message not sent')


def test_smtp_settings(smtp_settings):
    try:
        with smtplib.SMTP_SSL(smtp_settings.server, smtp_settings.port) as smtp:
            smtp.login(smtp_settings.username, smtp_settings.password)

            msg = EmailMessage()
            msg['Subject'] = 'Test message'
            msg['From'] = smtp_settings.username
            msg['To'] = 'recipient@example.com'
            msg.set_content('This is a test message to check the SMTP settings')

            smtp.send_message(msg)

        return True
    except Exception as e:
        print(e)
        return False, str(e)
