import logging

from django.core.management.base import BaseCommand
from src.Employees.models import CustomUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create or update a superuser"

    def handle(self, *args, **options):
        username = "admin"
        email = "admin@example.com"
        password = "admin"
        role = "superuser"

        user = CustomUser.objects.filter(username=username).first()

        if user:
            if user.role != role:
                user.role = role
                user.save()
                logger.warning("Superuser role updated successfully.")
            else:
                logger.warning("Superuser already exists.")
        else:
            CustomUser.objects.create_superuser(
                username=username, email=email, password=password, role=role
            )
            logger.warning("Superuser created successfully.")
