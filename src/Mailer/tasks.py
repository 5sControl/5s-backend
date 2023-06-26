from celery import shared_task

import smtplib
from email.message import EmailMessage

from django.db.models import Q

from src.Core.const import SERVER_URL

from src.Inventory.models import Items
from src.Mailer.models import Emails, SMTPSettings
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_low_stock_notification():
    """Checks low stock items and sends email notifications"""

    stock_items = Items.objects.filter(Q(status="Low stock level") | Q(status="Out of stock"))
    if len(stock_items) >= 1:
        email_list = Emails.objects.filter(is_active=True).values('email')
        subject = '5S Control Daily Low Stock Report'

        # email service check
        try:
            smtp_settings = SMTPSettings.objects.first()
        except SMTPSettings.DoesNotExist:
            logger.error('SMTP configuration is not defined')
            raise Exception('SMTP configuration is not defined')

        recipient_list = []
        for email in email_list:
            recipient_list.append(email.get('email'))

        if stock_items:
            # Build email content for all items with low stock
            message = 'The inventory level of the following items has fallen to a low stock level. We recommend that you take immediate action to replenish your stock to avoid stockouts or shortages.\nHere is the list of items and their corresponding quantities:\n'
            for item in stock_items:
                message += f"{item.name} : {item.current_stock_level} (low stock level: {item.low_stock_level})\n"

            message += f"\n{SERVER_URL}:3000/inventory\n\nYou are receiving this email because your email account was entered in 5S Control system to receive notifications regarding low stock levels of inventory."

            # Send email to all users
            with smtplib.SMTP_SSL(smtp_settings.server, smtp_settings.port) as smtp:
                smtp.login(smtp_settings.username, smtp_settings.password)

                email_message = EmailMessage()
                email_message['Subject'] = subject
                email_message['From'] = smtp_settings.username
                email_message['To'] = recipient_list
                email_message.set_content(message)

                smtp.send_message(email_message)

                logger.warning(f"Email sent to {recipient_list}")
        else:
            logger.warning(f'There is no critical stock level')

        return "success True"
