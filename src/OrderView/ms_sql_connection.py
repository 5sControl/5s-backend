import pyodbc

from rest_framework.exceptions import ValidationError

from src.OrderView.models import MsSQLConnection


class MsSqlService:
    def create_connection(self, connection_data):
        database_type = connection_data.get("database_type")
        server = connection_data["server"]
        database = connection_data["database"]
        username = connection_data["username"]
        password = connection_data["password"]

        self._check_database_exists(server, database, username, password)

        ms_sql_connection = MsSQLConnection(
            database_type=database_type,
            server=server,
            database=database,
            username=username,
            password=password,
        )
        ms_sql_connection.save()


    def _check_database_exists(self, server, database, username, password):
        driver = "{ODBC Driver 18 for SQL Server}"
        master_conn_str = self._get_connection_string(
            server, "master", username, password, driver
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
                    raise ValidationError({"detail": f"Database '{database}' does not exist"})
        except Exception as e:
            print("I dont now wht is this: ", e)
            raise ValidationError({"detail": f"Error when checking the existence of the database: {str(e)}"})

        conn_str = self._get_connection_string(
            server, database, username, password, driver
        )
        try:
            with pyodbc.connect(conn_str) as connection:
                pass
        except Exception as e:
            print("Database done 0_0")
            raise ValidationError({"detail": f"Database connection error: {str(e)}"})

    def get_database_connection(self):
        connection_data = (
            MsSQLConnection.objects.all()
            .values()
            .first()  # FIXME: should be by database type
        )

        server = connection_data["server"]
        database = connection_data["database"]
        username = connection_data["username"]
        password = connection_data["password"]
        driver = "{ODBC Driver 18 for SQL Server}"

        conn_str = self._get_connection_string(
            server, database, username, password, driver
        )

        connection = pyodbc.connect(conn_str)

        return connection

    def _get_connection_string(self, server, database, username, password, driver):
        return f"SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver};TrustServerCertificate=yes"  # noqa


ms_sql_service = MsSqlService()
