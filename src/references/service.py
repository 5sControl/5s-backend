import jwt
from django.contrib.auth.models import User
from jwt import InvalidTokenError
from config.settings.base import SECRET_KEY


def get_username_from_token(auth_header):
    """Function to extract the username from the JWT token."""
    if not auth_header:
        return None

    try:
        token = auth_header.split(' ')[1]
    except IndexError:
        return None

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')

        if not user_id:
            return None

        user = User.objects.get(id=user_id)
        return user.username if user else None

    except (InvalidTokenError, User.DoesNotExist):
        return None
