from rest_framework.response import Response
from rest_framework import status

from src.DatabaseConnections.models import DatabaseConnection


def check_database_connection(func):
    def wrapper(*args, **kwargs):
        if DatabaseConnection.objects.get(dbms="mssql") is not None:
            return func(*args, **kwargs)
        else:
            response_data = {
                "status": False,
                "message": "database connection doesnt exist",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    return wrapper
