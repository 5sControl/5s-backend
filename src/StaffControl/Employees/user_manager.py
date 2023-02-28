from django.contrib.auth.models import User

from src.core.logger import logger

class UserManager:
    def create_superuser(self, username: str, password: str):
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username,
                                          email="owner@example.com",
                                          password=password,
                                          is_staff=False,
                                          is_superuser=True
                                          )
            logger.info(
                f"Superuser created successfully. Username: {username} Password: {password}"
                )
        else:
            logger.info("Superuser already exists")
    
    def create_staff(self, username: str, password: str):
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username,
                                     "staff@example.com",
                                     password,
                                     is_staff=True,
                                     is_superuser=False
                                     )
            logger.info(
                f"Staff user created successfully. Username: {username} Password: {password}"
                )
        else:
            logger.info("User already exists")
    
    def create_worker(self, username: str, password: str):
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username,
                                     email="worker@example.com",
                                     password=password,
                                     is_staff=False, 
                                     is_superuser=False
                                     )
            logger.info(
                f"Worker user created successfully. Username: {username} Password: {password}"
            )
        else:
            logger.info("User already exists")

