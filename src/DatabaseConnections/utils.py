from rest_framework.response import Response
from rest_framework import status

from src.DatabaseConnections.models import ConnectionInfo

import requests


def check_database_connection(func):
    def wrapper(*args, **kwargs):
        connection = ConnectionInfo.objects.get(type="database")

        if connection is not None:
            return func(*args, **kwargs)
        else:
            response_data = {
                "status": False,
                "message": "database connection doesnt exist",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    return wrapper


def get_all_items_odoo():
    """Returns a list of all items from the ODOO"""
    try:
        connection = ConnectionInfo.objects.filter(type="api").values('host', 'database', 'username', 'password')[0]
        if connection['host'] is None:
            raise ValueError("Missing connection host")
        if connection['username'] is None:
            raise ValueError("Missing connection username")
        if connection['password'] is None:
            raise ValueError("Missing connection password")
        if connection['database'] is None:
            raise ValueError("Missing connection database")
        response = requests.get(f"{connection['host']}/min_max/all_items")
        if response.status_code == 200:
            data = response.json().get('data')

            return data
        else:
            return Response({"error": "Failed to fetch data from external service"}, status=response.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
