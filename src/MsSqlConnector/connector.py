import pyodbc

from rest_framework.exceptions import ValidationError

from src.MsSqlConnector.models import DatabaseConnection


class MsSqlConnector:
    def __init__(self):
        self.driver = "{ODBC Driver 17 for SQL Server}"

    def create_connection(self, connection_data):
        database_type = connection_data.get("database_type")
        server = connection_data["server"]
        database = connection_data["database"]
        username = connection_data["username"]
        password = connection_data["password"]

        self._is_database_connection_is_stable(server, database, username, password)
        self._is_database_connection_exist(server, database, username)

        ms_sql_connection = DatabaseConnection(
            database_type=database_type,
            server=server,
            database=database,
            username=username,
            password=password,
        )
        ms_sql_connection.save()

        connection = {
            "id": ms_sql_connection.id,
            "database_type": ms_sql_connection.database_type,
            "server": ms_sql_connection.server,
            "database": ms_sql_connection.database,
            "username": ms_sql_connection.username,
        }
        return connection

    def _is_database_connection_is_stable(self, server, database, username, password):
        master_conn_str = self._get_connection_string(
            server, "master", username, password, self.driver
        )
        try:
            with pyodbc.connect(master_conn_str) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM sys.databases WHERE name = ?", (database,)
                )
                exists = cursor.fetchone()[0] == 1
                if not exists:
                    print("Connection does not exist")
                    raise ValidationError(
                        {"detail": f"Database '{database}' does not exist"}
                    )
        except Exception as e:
            print("I dont now wht is this: ", e)
            raise ValidationError(
                {
                    "detail": f"Error when checking the existence of the database: {str(e)}"
                }
            )

        conn_str = self._get_connection_string(
            server, database, username, password, self.driver
        )
        try:
            with pyodbc.connect(conn_str) as connection:
                pass
        except Exception as e:
            print("Database done 0_0")
            raise ValidationError({"detail": f"Database connection error: {str(e)}"})

    def _is_database_connection_exist(self, server, database, username):
        if DatabaseConnection.objects.filter(
            server=server, database=database, username=username
        ):
            raise ValidationError({"detail": "Database connection already in database"})

    def get_database_connection(self):
        connection_data = (
            DatabaseConnection.objects.all()
            .values()
            .first()  # FIXME: should be by database type
        )

        server = connection_data["server"]
        database = connection_data["database"]
        username = connection_data["username"]
        password = connection_data["password"]

        conn_str = self._get_connection_string(
            server, database, username, password, self.driver
        )

        connection = pyodbc.connect(conn_str)

        return connection

    def _get_connection_string(self, server, database, username, password, driver):
        return f"SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver};TrustServerCertificate=yes"  # noqa

    def get_conections(self):
        return DatabaseConnection.objects.all()

    def delete_connection(self, id):
        DatabaseConnection.objects.get(id=id).delete()
        return True


connector = MsSqlConnector()
