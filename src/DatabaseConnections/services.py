import logging
import requests

from typing import Any, Dict

from src.DatabaseConnections.models import ConnectionInfo
from src.DatabaseConnections.repositories.ms_repository import WinHRepository

logger = logging.getLogger(__name__)


class CreateConnectionManager:
    def create_api_connection(self, credentials: Dict[str, Any]) -> bool:
        host = credentials["host"]

        connection, created = ConnectionInfo.objects.update_or_create(
            type="api",
            defaults={"is_active": True, "host": host},
        )

        return created or connection

    def create_database_connection(self, credentials: Dict[str, Any]) -> bool:
        dbms: str = credentials.get("dbms", "mssql")
        server: str = credentials["server"]
        database: str = credentials["database"]
        username: str = credentials["username"]
        password: str = credentials["password"]
        port: int = credentials["port"]

        if dbms == "mssql":
            is_stable: bool = WinHRepository().is_stable(
                server, database, username, password, port
            )
            if not is_stable:
                logger.critical("Database connection is not stable")
                return False
        elif dbms == "postgres":
            logger.critical("Database connection is not implemented")
            raise ValueError("Not implemented")
        else:
            logger.critical("Type of dbms is not supported")
            return False

        connection, created = ConnectionInfo.objects.update_or_create(
            type="database",
            defaults={
                "is_active": True,
                "server": server,
                "database": database,
                "username": username,
                "password": password,
                "port": port,
            },
        )

        return created or connection

    def delete_connection(self, connection_id: int) -> bool:
        try:
            ConnectionInfo.objects.get(id=connection_id).delete()
            return True
        except ConnectionInfo.DoesNotExist:
            return False


def get_data_five_control(type_data):
    connection = ConnectionInfo.objects.filter(is_active=True, erp_system="5s_control").first()
    host = connection.host
    port = connection.port

    url = f"{host}:{port}/production-catalog/{type_data}"
    response = requests.get(url)
    return response.json(), response.status_code
