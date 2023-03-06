from django.db import connections
from decouple import config
def create_database_connection(data):
    print(config("SQL_ENGINE", ""))

    newDatabase = {}

    db_name = data['db_name']
    db_user = data['db_user']
    db_password = data['db_password']
    db_host = data['db_host']
    db_port = data['db_port']

    try:
        database_id = "ms_sql"
        newDatabase["id"] = database_id
        newDatabase['ENGINE'] = 'sql_server.pyodbc',
        newDatabase['NAME'] = db_name
        newDatabase['USER'] = db_user
        newDatabase['PASSWORD'] = db_password
        newDatabase['HOST'] = db_host
        newDatabase['PORT'] = db_port
        newDatabase['OPTIONS'] = {
                    'driver': 'ODBC Driver 17 for SQL Server',
        }
        connections.databases[database_id] = newDatabase
    except Exception:
        return {
            "status": False,
            "message": "Cannot connect to new database"
        }
    else:
        return {
            "status": True,
            "message": "The connection was installed successfully"
        }