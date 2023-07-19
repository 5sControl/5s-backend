from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class DatabaseConnection(models.Model):
    DBMS_CHOICES = (
        ("postgres", "PostgreSQL"),
        ("mssql", "Microsoft SQL Server"),
    )

    database_type = models.CharField(max_length=50, default="OrderView")
    server = models.CharField(max_length=200)
    database = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=500)
    port = models.IntegerField(default=1433)
    dbms = models.CharField(
        max_length=50, choices=DBMS_CHOICES, default="mssql"
    )
    is_active = models.BooleanField(default=True, unique=True)

@receiver(pre_save, sender=DatabaseConnection)
def update_active_status(sender, instance, **kwargs):
    if not instance.pk:
        sender.objects.update(is_active=False)
        instance.is_active = True