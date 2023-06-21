import os
import smtplib
from datetime import datetime
from datetime import time

from email.message import EmailMessage

from src.CompanyLicense.models import Company
from src.Mailer.models import SMTPSettings, WorkingTime


def send_email_to_suppliers(item, image_path):
    """Send email to supplier"""
    try:
        if item.suppliers is None or item.suppliers.contact_email is None:
            raise ValueError("Missing contact email")
        my_company = Company.objects.filter(my_company=True).order_by('-id').first()
        count_order = item.order_quantity

        if item.name is None:
            raise ValueError("Missing item name")
        if item.suppliers.name_company is None:
            raise ValueError("Missing supplier name")
        if my_company.name_company is None:
            raise ValueError("Missing my company name")
        if my_company.country is None:
            raise ValueError("Missing my company country")
        if my_company.state is None:
            raise ValueError("Missing my company state")
        if my_company.city is None:
            raise ValueError("Missing my company city")
        if my_company.first_address is None:
            raise ValueError("Missing my company first_address")
        if my_company.contact_phone is None:
            raise ValueError("Missing my company phone")
        if my_company.contact_email is None:
            raise ValueError("Missing my company email")

    except Exception as exc:
        print(f"Not enough parameters to send notification: {exc}")
        return
    address = f"{my_company.country} {my_company.state} {my_company.city} {my_company.first_address}"
    subject = f"Urgent Reorder Request: Low Stock Level Notification - {item.name}"
    message = f"Dear {item.suppliers.name_company}!\nBy this message we notify you of our urgent need to reorder a specific item due to its low stock level.\nItem Details:\nItem Name: {item.name},\nQuantity Needed: {count_order}\n\nPlease ensure that the additional order is promptly processed and dispatched to us to avoid any disruptions to our operations. We kindly request your immediate attention to this matter.\n\nCompany Information:\nCompany Name: {my_company.name_company}\nAddress: {address}\nPhone: {my_company.contact_phone}\nEmail: {my_company.contact_email}\n\nPlease note that this message is automatically generated, and there is no need to reply to it. However, if you have any questions or require further information, please feel free to contact us using the provided company details.We appreciate your ongoing partnership and your commitment to providing quality products and services. Thank you for your prompt attention to this matter.\nBest regards, {my_company.name_company}\n"

    image_name = image_path.split('/')[-1]

    recipient_list = [item.suppliers.contact_email]
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

            file_path = item.suppliers.file
            if file_path and len(file_path) > 5:
                file_name = file_path.name
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', f'images/{file_name}')
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    email_message.add_attachment(file_data, maintype='application',
                                                 subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                                 filename=file_name)
                else:
                    print("File does not exist:", file_path)
            else:
                print("File path is not provided")

            smtp.send_message(email_message)

    else:
        print('Working time limit, message not sent')
