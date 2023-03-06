import pymssql


class DBConn:

    def get_connection(self, data):

        db_name = data['db_name']
        db_user = data['db_user']
        db_password = data['db_password']
        db_host = data['db_host']
        db_port = data['db_port']

        conn = pymssql.connect(server=db_host, database=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()

        # execute query to retrieve one record from specified table
        query = f"SELECT TOP 1 * FROM Skany"
        cursor.execute(query)
        record = cursor.fetchone()

        # close connection and return record
        conn.close()
        return record

db_conn = DBConn()