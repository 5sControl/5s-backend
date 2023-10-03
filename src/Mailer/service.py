import os
import requests

import smtplib
from email.message import EmailMessage

from datetime import datetime
from datetime import time

from celery import shared_task

from src.Mailer.models import SMTPSettings, WorkingTime
from src.DatabaseConnections.models import ConnectionInfo


@shared_task
def send_notification_email(item, count, image_path, item_status):
    """Send notification email"""

    if item['subject'] is None:
        raise ValueError("Missing item subject")

    to_emails = item.get('to_emails', [])
    to_emails = to_emails if to_emails is not None else []

    copy_emails = item.get('copy_emails')
    copy_emails = copy_emails if copy_emails is not None else []

    recipient_list = list(set(to_emails + copy_emails))

    used_algorithm = item["object_type"]
    message = ""
    subject = f"{item['subject']}"
    if item_status == 'Low stock level':
        message = f"Current stock of {item['name']}: {count} {used_algorithm}. Low stock level of {item['name']}: {item['low_stock_level']}. The inventory level of {item['name']} in your stock has fallen to a low level. This means that there are only a limited number of units left in stock and that the item may soon become unavailable. To avoid any inconvenience, we recommend that you take action to replenish your stock of {item['name']} as soon as possible. You are receiving this email because your email account was entered in 5S Control system to receive notifications regarding low stock levels of inventory."

        # send notification ODOO
        try:
            odoo_notification(message)
        except Exception as exception:
            print(f"Odoo notification failed: {exception}")

    image_name = image_path.split('/')[-1]

    # email service check
    try:
        smtp_settings = SMTPSettings.objects.first()
    except SMTPSettings.DoesNotExist:
        raise Exception('SMTP configuration is not defined')

    # Check if work time
    work_time = WorkingTime.objects.last()
    if work_time is None:
        start_time = time(0, 0)
        end_time = time(23, 59)
    else:
        start_time = work_time.time_start
        end_time = work_time.time_end

    today = datetime.now().time()
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
    """Test checking for correctness smtp server"""
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


@shared_task
def odoo_notification(message: str):
    """Send ODOO notification"""

    connection = ConnectionInfo.objects.filter(type="api").values('host', 'database', 'username', 'password')[0]

    if connection['host'] is None:
        raise ValueError("Missing connection host")
    if connection['username'] is None:
        raise ValueError("Missing connection username")
    if connection['password'] is None:
        raise ValueError("Missing connection password")
    if connection['database'] is None:
        raise ValueError("Missing connection database")

    session = requests.Session()
    response = session.post(f"{connection['host']}/web/session/authenticate", json={
        "jsonrpc": "2.0",
        "params": {
            "db": connection['database'],
            "login": connection['username'],
            "password": connection['password']
        }
    })

    if response.ok:
        data = {
            "message": message
        }
        send_message_endpoint = "/min_max/send_message"
        response = session.post(f"{connection['host']}{send_message_endpoint}", json=data)
    else:
        raise "Authentication failed!"

