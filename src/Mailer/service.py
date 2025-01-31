import os
import requests

import smtplib
from email.message import EmailMessage

from datetime import datetime
from datetime import time

from celery import shared_task

from src.CameraAlgorithms.services.cameraalgorithm import stop_camera_algorithm, create_single_camera_algorithms
from src.Mailer.models import SMTPSettings, WorkingTime
from src.DatabaseConnections.models import ConnectionInfo
from src.CameraAlgorithms.models.algorithm import CameraAlgorithm


from decouple import config

NGROK_URL = config("NGROK_URL")


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

    subject = f"{item['subject']}"

    message = ""

    if item_status == "Out of stock":
        message = f"{item['name']} is currently out of stock.\n To avoid any inconvenience, we recommend that " \
                  f"you take action to replenish your stock of {item['low_stock_level']} as soon as possible." \
                  f"\n\n{NGROK_URL}inventory/\n\n You are receiving this email because your email account was " \
                  f"entered in 5S Control system to receive notifications regarding low stock levels of inventory."

    if item_status == 'Low stock level':
        message = f"Current stock of {item['name']}: {count} {used_algorithm}. Low stock level of {item['name']}: " \
                  f"{item['low_stock_level']}. The inventory level of {item['name']} in your stock has " \
                  f"fallen to a low level. This means that there are only a limited number of units left in stock " \
                  f"and that the item may soon become unavailable. To avoid any inconvenience, we recommend that " \
                  f"you take action to replenish your stock of {item['name']} as soon as possible." \
                  f"\n\n{NGROK_URL}inventory\n\nYou are receiving this email because your email account was " \
                  f"entered in 5S Control system to receive notifications regarding low stock levels of inventory."

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


def work_time_min_max():
    algorithm = "min_max_control"
    all_cameras = []

    all_algorithm = CameraAlgorithm.objects.filter(algorithm__name__iexact=algorithm)
    for algorithms in all_algorithm:
        pid_process = algorithms.process_id
        # STOP процесс
        stop_camera_algorithm(pid_process)
        all_cameras.append(algorithms.camera_id)

    return task_start_minmax(all_cameras, algorithm)


def task_start_minmax(all_cameras, algorithm):
    for camera in all_cameras:
        create_single_camera_algorithms({'ip': camera}, {"name": algorithm})


def check_work_time():
    working_time = WorkingTime.objects.last()
    if working_time is not None:
        time_start = working_time.time_start
        time_end = working_time.time_end
        current_time = datetime.now().time()
        status = time_start <= current_time <= time_end
        return {"status": status, "time_start": time_start, "time_end": time_end}
    else:
        return {"status": True}


def text_message_reset_password(code, language_code="en"):
    support_email = "support@5scontrol.com"
    data_text = {
        "en": f"Password Reset for your 5SControl Account\n\nHello!\nYou requested a password reset for your account."
              f"\nTo complete the password reset, please copy and enter the following verification code on the "
              f"password reset page: \n\n{code}\n\nThis code is valid for 15 minutes. If you did not request a "
              f"password reset, please ignore this email.\nIf you have any questions or concerns, please contact "
              f"our support team at {support_email}.\nSincerely, 5sControl.",
        "ru": f"Сброс пароля для вашей учетной записи 5SControl.\n\nЗдравствуйте!\nВы запросили сброс пароля для "
              f"своей учетной записи.\nДля завершения сброса пароля, пожалуйста, скопируйте и введите следующий код "
              f"подтверждения на странице сброса пароля:\n\n{code}\n\nЭтот код действителен в течение 15 минут. "
              f"Если вы не запрашивали сброс пароля, пожалуйста, проигнорируйте это письмо.\nЕсли у вас возникли "
              f"вопросы или проблемы, свяжитесь с нашей службой поддержки по адресу {support_email}.\n"
              f"С уважением, 5sControl.",
        "pl": f"Reset hasła do Twojego konta 5SControl \n\nCześć!\nPoprosiłeś o zresetowanie hasła do swojego konta."
              f"\nAby ukończyć resetowanie hasła, skopiuj i wprowadź następujący kod weryfikacyjny na stronie "
              f"resetowania hasła:\n\n{code}\n\nTen kod jest ważny przez 15 minut. Jeśli nie prosiłeś o resetowanie "
              f"hasła, zignoruj ten e-mail.\nJeśli masz jakieś pytania lub wątpliwości, skontaktuj się z naszym "
              f"zespołem pomocy technicznej pod adresem {support_email}. Z poważaniem, 5sControl."
    }
    text_answer = data_text.get(language_code)
    if not text_answer:
        text_answer = data_text.get("en")
    return text_answer
