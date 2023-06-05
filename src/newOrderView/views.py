from typing import Dict, List, Any

from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse

from src.Core.paginators import OrderViewPaginnator
from src.MsSqlConnector.connector import connector as connector_service

from .services.order_services import OrderServices


class GetOperation(generics.GenericAPIView):
    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        result: List[Dict[str, Any]] = OrderServices.get_operations(from_date, to_date)

        return JsonResponse(data=result, status=status.HTTP_200_OK, safe=False)


class GetOrders(generics.GenericAPIView):
    pagination_class = OrderViewPaginnator

    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        result: List[Dict[str, str]] = OrderServices.get_order(from_date, to_date)

        return JsonResponse(result, status=status.HTTP_200_OK, safe=False)


class GetOrderByDetail(generics.GenericAPIView):
    pagination_class = OrderViewPaginnator

    @connector_service.check_database_connection
    def get(self, request):
        operation_id: int = request.GET.get("operation")

        result: Dict[str, Any] = OrderServices.get_order_by_details(operation_id)

        return JsonResponse(data=result, status=status.HTTP_200_OK)
