from src.Order.database_conn import db_conn


class OrderService:
    def get_skany_data(self):
        conn = db_conn.get_cursor()
        cursor = conn.cursor()
        query = f"SELECT TOP 1 * FROM Skany"
        cursor.execute(query)
        record = cursor.fetchone()

        conn.close()
        return record


order_service = OrderService()
