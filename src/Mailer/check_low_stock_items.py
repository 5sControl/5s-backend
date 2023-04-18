from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend

from src.Algorithms.utils import yolo_proccesing
from src.Inventory.models import Items
from src.Mailer.models import Emails, SMTPSettings


def run():
    """Checks low stock items and sends email notifications"""

    low_stock_items = Items.objects.filter(status="Low stock level").exclude(status="Out of stock")
    if low_stock_items:
        email_list = Emails.objects.filter(is_active=True).values('email')
        subject = 'Daily Low Stock Report'
        server_url = yolo_proccesing.get_algorithm_url()

        # email service check
        try:
            smtp_settings = SMTPSettings.objects.first()
        except SMTPSettings.DoesNotExist:
            raise Exception('SMTP configuration is not defined')

        recipient_list = []
        for email in email_list:
            recipient_list.append(email.get('email'))

        if low_stock_items:
            # Build email content for all items with low stock
            message = 'The inventory level of the following items has fallen to a low stock level. We recommend that you take immediate action to replenish your stock to avoid stockouts or shortages.\nHere is the list of items and their corresponding quantities:\n'
            for item in low_stock_items:
                message += f"{item.name} - {item.current_stock_level}\n"

            message += f"\n{server_url}:3000/inventory"
            # Send email to all users
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
    else:
        print(f'There is no critical stock level')
