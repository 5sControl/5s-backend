import pyodbc

from src.OrderView.models import MsSQLConnection


def get_database_connection(database_type):
    connection_data = (
        MsSQLConnection.objects.filter(database_type=database_type).values().first()
    )

    server = connection_data["server"]
    database = connection_data["database"]
    username = connection_data["username"]
    password = connection_data["password"]
    driver = "{ODBC Driver 18 for SQL Server}"

    conn_str = f"SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver};TrustServerCertificate=yes"

    connection = pyodbc.connect(conn_str)

    return connection


def skany(database_type):
    with get_database_connection(database_type) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Skany")
        for row in cursor:
            print(row)
