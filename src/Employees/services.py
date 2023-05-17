import logging

from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class UserManager:
    def create_superuser(self, username: str, password: str):
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=None,
                password=password,
                is_staff=False,
                is_superuser=True,
            )
            logger.warning(
                f"Superuser created successfully. Username: {username} Password: {password}"
            )
        else:
            logger.warning("Superuser already exists")

    def create_admin(self, username: str, password: str):
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=None,
                password=password,
                is_staff=True,
                is_superuser=False,
            )
            logger.warning(
                f"Staff user created successfully. Username: {username} Password: {password}"
            )
        else:
            logger.warning("User already exists")

    def create_worker(self, username: str, password: str):
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=None,
                password=password,
                is_staff=False,
                is_superuser=False,
            )
            logger.warning(
                f"Worker user created successfully. Username: {username} Password: {password}"
            )
        else:
            logger.warning("User already exists")


user_manager = UserManager()
