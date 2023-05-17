from django.contrib.auth.models import User


def create_user(username: str, password: str) -> User:
    return User.objects.create_user(username=username, password=password, is_superuser=True)
