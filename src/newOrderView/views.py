from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from src.Core.paginators import OrderViewPaginnator
from src.MsSqlConnector.connector import connector as connector_service

from .services.order_services import services


class GetZlecnieList(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderViewPaginnator

    @connector_service.check_database_connection
    def get(self, request):
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")

        result = services.get_order(from_date, to_date)

        return Response(result, status=200)