from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from src.DatabaseConnections.models import ConnectionInfo

import requests


@receiver(post_save, sender=User)
def send_user_data_to_service(sender, instance, created, **kwargs):

    connection = ConnectionInfo.objects.get(erp_system="5s_control")
    url = f"{connection.host}:{connection.port}/items/employee/"
    if created:
        user_data = {
            'id': instance.id,
            'username': instance.username,
        }

        try:
            response = requests.post(url, json=user_data)
            print("Send data to DB erp", response)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to send user data: {e}")
