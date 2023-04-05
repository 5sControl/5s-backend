from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from src.Core.logger import logger


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            logger.info(
                f"Superuser created successfully. Username: admin Password: admin"
            )
        else:
            logger.info("Superuser already exists")
