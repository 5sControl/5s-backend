from celery import shared_task
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend

from django.db.models import Q

from src.Algorithms.utils import yolo_proccesing
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
        server_url = yolo_proccesing.get_algorithm_url()

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

            message += f"\n{server_url}:3000/inventory\n\nYou are receiving this email because your email account was entered in 5S Control system to receive notifications regarding low stock levels of inventory."
            # Send email to all users
            connection = EmailBackend(
                host=smtp_settings.server,
                port=smtp_settings.port,
                username=smtp_settings.username,
                password=smtp_settings.password,
                use_tls=smtp_settings.email_use_tls,
                use_ssl=smtp_settings.email_use_ssl,
            )
            try:
                send_mail(
                    subject,
                    message,
                    smtp_settings.username,
                    recipient_list,
                    fail_silently=False,
                    connection=connection,
                )
                logger.info(f"Email sent to {recipient_list}")
            except Exception as e:
                logger.error(f"Email sending failed with error: {e}")
        else:
            logger.info(f'There is no critical stock level')

        return "success True"
