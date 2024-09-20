import requests
import json
from django.http import JsonResponse

from src.DatabaseConnections.models import ConnectionInfo


def authenticate_user(host, database, username, password):
    session = requests.Session()

    response = session.get(f"{host}/web/login")

    if response.status_code != 200:
        raise ValueError(f"Error receiving CSRF token: {response.status_code}")

    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": database,
            "login": username,
            "password": password,
        },
        "id": 1,
    }
    headers = {
        'Content-Type': 'application/json',
        'X-CSRF-Token': session.cookies.get('csrf_token')
    }

    response = session.post(f"{host}/web/session/authenticate", json=data, headers=headers)

    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data.get('result').get('uid')
        except ValueError:
            raise ValueError(f"Authorization error: {response.status_code} - {response.text}")
    else:
        raise ValueError(f"Authorization error: {response.status_code} - {response.text}")


def odoo_login():

    connection = ConnectionInfo.objects.filter(is_active=True, erp_system="odoo")
    url = connection.host
    db = connection.database
    username = connection.username
    password = connection.password

    user_id = authenticate_user(url, db, username, password)

    if user_id:
        return JsonResponse({"success": True, "user_id": user_id}, status=200)
    else:
        return JsonResponse({"success": False, "error": "Invalid credentials"}, status=403)
