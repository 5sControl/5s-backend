import logging

from django.core.management.base import BaseCommand
from  src.Employees.models import CustomUser
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(username="admin").exists():
            CustomUser.objects.create_superuser("admin", "admin@example.com", "admin")
            logger.warning(
                "Superuser created successfully. Username: admin Password: admin"
            )
        else:
            logger.warning("Superuser already exists")
