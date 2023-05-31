from typing import List, Any, Tuple, Dict

from src.MsSqlConnector.connector import connector as connector_service


        result: List[Dict[str, Any]] = [
            {"id": item[0], "order": item[1].strip()} for item in data
        ]

        return result

class OrderServices:
    def get_order(self, from_date: str, to_date: str):
        query: str = f'''
            SELECT sk.indeks, sk.data, st.OperationID, st.OperationName
            FROM skany sk
            JOIN Stanowiska st ON sk.stanowisko = st.indeks
            WHERE 1=1 
        '''

        connection = connector_service.get_database_connection()
        params: List[Any] = []

        if from_date and to_date:
                query += " AND sk.data >= ? AND sk.data <= ?"
                params.extend([from_date, to_date])
        print(query, params)

        results = connector_service.executer(
            connection=connection,
            query=query,
            params=params,
        )
        print(results)
        return result


services = OrderServices()

class OrderServices:
    def get_operation_by_date(self, from_date: str, to_date: str):

        
        


services = OrderServices()

