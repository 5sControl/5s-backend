from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class ConnectionInfo(models.Model):
    TYPE_CHOICES = (
        ("database", "Database"),
        ("api", "API"),
    )

    DBMS_CHOICES = (
        ("postgres", "PostgreSQL"),
        ("mssql", "Microsoft SQL Server"),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="database")
    dbms = models.CharField(max_length=50, choices=DBMS_CHOICES, default="mssql")
    is_active = models.BooleanField(default=True)
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
    if instance.is_active:
        sender.objects.exclude(pk=instance.pk).update(is_active=False)
