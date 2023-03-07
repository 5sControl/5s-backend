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
        orders = OrderService.get_skany_data()
        return Response(orders, status=status.HTTP_200_OK)

