from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import requests


class ConnectionInfo(models.Model):
    TYPE_CHOICES = (
        ("database", "Database"),
        ("api", "API"),
    )

    DBMS_CHOICES = (
        ("postgres", "PostgreSQL"),
        ("mssql", "Microsoft SQL Server"),
        ("manifest", "Manifest"),
    )

    ERP_SYSTEM_CHOICES = (
        ("odoo", "ODOO"),
        ("winkhaus", "Winkhaus"),
        ("manifest", "Manifest"),
        ("5s_control", "5sControl"),
    )

    erp_system = models.CharField(max_length=20, choices=ERP_SYSTEM_CHOICES, default="winkhaus")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="database")
    dbms = models.CharField(max_length=50, choices=DBMS_CHOICES, default="mssql")
    is_active = models.BooleanField(default=True)
    used_in_orders_view = models.BooleanField(default=False)
    #  api
    host = models.CharField(max_length=250, blank=True, null=True)
    #  db
    server = models.CharField(max_length=200, blank=True, null=True)
    database = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.server or self.host}"

    class Meta:
        verbose_name = "Connection Info"
        verbose_name_plural = "Connection Infos"
        db_table = "connection_info"


@receiver(pre_save, sender=ConnectionInfo)
def update_active_status(sender, instance, **kwargs):
    if instance.used_in_orders_view:
        sender.objects.exclude(pk=instance.pk).update(used_in_orders_view=False)

    if instance.is_active:
        sender.objects.exclude(pk=instance.pk).update(is_active=False)

        if instance.erp_system == "manifest":

            url = f"{instance.host}rest/signin"
            data = {
                'email': instance.username,
                'password': instance.password
            }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'PostmanRuntime/7.37.3',
            }

            try:
                response = requests.post(url, json=data, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                token = response_data.get('user').get('token')
            except requests.exceptions.RequestException as e:
                raise ValueError(f"Error while requesting token: {e}")

        elif instance.erp_system == "odoo":
            from src.odoo_api.service import authenticate_user
            user_id = authenticate_user(instance.host, instance.database, instance.username, instance.password)
            if user_id:
                print(f"Authorization in Odoo is successful, user_id: {user_id}")
            else:
                raise ValueError("Login to Odoo failed.")
