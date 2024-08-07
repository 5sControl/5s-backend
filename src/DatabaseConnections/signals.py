from django.db.models.signals import pre_save
from django.dispatch import receiver
from src.DatabaseConnections.models import ConnectionInfo
from src.manifest_api.models import ManifestConnection


@receiver(pre_save, sender=ConnectionInfo)
def update_active_status(sender, instance, **kwargs):
    if instance.pk is None:
        if instance.erp_system == "manifest":
            handle_manifest_connection(instance)


def handle_manifest_connection(instance):
    manifest_connection = ManifestConnection()

    manifest_connection.host = instance.host
    manifest_connection.username = instance.username
    manifest_connection.password = instance.password
    manifest_connection.save()
