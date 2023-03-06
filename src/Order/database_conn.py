import pymssql

from src.Order.models import DatabaseConnection


class DBConn:
    def save_conn_data(self, data):
        db_name = data["db_name"]
        db_user = data["db_user"]
        db_password = data["db_password"]
        db_host = data["db_host"]

        try:
            if not self.check_connection(db_name, db_user, db_password, db_host):
                raise Exception("Could not connect to database")

            newDatabaseConnection = DatabaseConnection(
                db_name=db_name,
                db_user=db_user,
                db_password=db_password,
                db_host=db_host
            )
            newDatabaseConnection.save()
        except Exception:
            return {
                "status": False,
                "message": "Database connection doest created successfully",
            }
        return {
            "status": True,
            "message": "Database connection created successfully",
        }
    
    def check_connection(self, db_name, db_user, db_password, db_host):
        try:
            conn = pymssql.connect(
                server=db_host, database=db_name, user=db_user, password=db_password
            )
            print("Connection: ", conn)
            cursor = conn.cursor()
        except Exception:
            return False
        return True

    def get_cursor(self,):
        cred = DatabaseConnection.objects.first()
        conn = pymssql.connect(
                server=cred.db_host, database=cred.db_name, user=cred.db_user, password=cred.db_password
            )
        return conn
        

db_conn = DBConn()
