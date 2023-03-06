from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from src.Order.serializer import DatabaseConnectionSerializer

from src.Order.services import OrderService
from src.Order.database_conn import db_conn

class GetOrderApiView(generics.GenericAPIView):
    """
    Get order records from ms sql
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = OrderService.get_order_data()
        return Response(orders, status=status.HTTP_200_OK)


class DatabaseConnectionApiView(generics.GenericAPIView):
    """
    Get credentials to connect to the ms sql server
    """

    serializer_class = DatabaseConnectionSerializer

    def post(self, request, *args, **kwargs):
        result = db_conn.get_connection(request.data)
        if result:
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
