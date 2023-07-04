from typing import Any, Dict, List

from src.DatabaseConnections.models import DatabaseConnection
from src.DatabaseConnections.repositories.ms_repository import MsSqlServerRepository


class DatabaseConnectionManager:
    def create_connection(self, credentials: Dict[str, Any], db_type: str) -> bool:
        server = credentials["server"]
        database = credentials["database"]
        username = credentials["username"]
        password = credentials["password"]
        port = credentials["port"]

        if DatabaseConnection.objects.filter(
            server=server, database=database, username=username, port=port
        ).exists():
            return False

        if db_type == "mssql":
            if MsSqlServerRepository().is_stable(
                server, database, username, password, port
            ):
                return True

        return False

    def get_connections(self) -> List[Dict[str, Any]]:
        return DatabaseConnection.objects.all()

    def delete_connection(self, connection_id: int) -> bool:
        try:
            DatabaseConnection.objects.get(id=connection_id).delete()
            return True
        except DatabaseConnection.DoesNotExist:
            return False
