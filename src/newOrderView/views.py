from typing import Dict, List, Any

from rest_framework import generics
from rest_framework.response import Response

from src.Core.paginators import OrderViewPaginnator
from src.MsSqlConnector.connector import connector as connector_service

from .services.order_services import services


class GetOperation(generics.GenericAPIView):
    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        result: List[Dict[str, Any]] = services.get_operations(from_date, to_date)

        return Response(result, status=200)


class GetOrders(generics.GenericAPIView):
    pagination_class = OrderViewPaginnator

    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        result: List[Dict[str, Any]] = services.get_order(from_date, to_date)

        return Response(result, status=200)


class GetOrderByDetail(generics.GenericAPIView):
    pagination_class = OrderViewPaginnator

    @connector_service.check_database_connection
    def get(self, request):
        operation_id: int = request.GET.get("operation")

        result = services.get_order_by_details(operation_id)

        return Response(result, status=200)
