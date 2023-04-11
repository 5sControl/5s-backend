from datetime import datetime, time
from django.utils import timezone
from rest_framework import status

from rest_framework.response import Response

from src.Mailer.models import SMTPSettings, NotificationsSent


def send_email_within_hours(start_time, end_time):
    """
    Decorator to send email only within certain hours of the day
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            now = timezone.now()
            start_datetime = timezone.make_aware(datetime.combine(now.date(), start_time))
            end_datetime = timezone.make_aware(datetime.combine(now.date(), end_time))
            if now >= start_datetime and now <= end_datetime:
                # Check if a message was already sent today
                recipients = kwargs.get('recipient_list')
                if recipients:
                    sent_today = NotificationsSent.objects.filter(
                        recipients__in=recipients,
                        date_created__date=timezone.now().date()
                    ).exists()
                    if sent_today:
                        return Response({'detail': 'A message has already been sent today'},
                                        status=status.HTTP_400_BAD_REQUEST)

                # Call the wrapped function
                response = func(*args, **kwargs)

                # If the email was sent successfully, save the notification record
                if response.status_code == status.HTTP_200_OK:
                    for recipient in recipients:
                        NotificationsSent.objects.create(recipients=recipient)

                return response
            else:
                return Response({'detail': 'Emails can only be sent between {} and {}'.format(start_time, end_time)},
                                status=status.HTTP_400_BAD_REQUEST)

        return wrapper

    return decorator
