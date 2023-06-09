from typing import Dict, List, Any

from django.http import JsonResponse
from django.core.cache import cache

from rest_framework import generics, status

from src.Core.paginators import OrderViewPaginnator
from src.MsSqlConnector.connector import connector as connector_service

from .services.order_services import OrderServices
from .utils import generate_hash


class GetOperation(generics.GenericAPIView):
    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        key: str = generate_hash("get_operation", from_date, to_date)
        response = cache.get(key)

        if response is None:
            response: List[Dict[str, Any]] = OrderServices.get_operations(
                from_date, to_date
            )
            cache.set(key, response, timeout=120)

        return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)


class GetOrders(generics.GenericAPIView):
    pagination_class = OrderViewPaginnator

    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        key: str = generate_hash("get_order", from_date, to_date)
        response = cache.get("get_order_" + key)

        if response is None:
            response: List[Dict[str, str]] = OrderServices.get_order(from_date, to_date)
            cache.set(key, response, timeout=120)

        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


class GetOrderByDetail(generics.GenericAPIView):
    pagination_class = OrderViewPaginnator

    @connector_service.check_database_connection
    def get(self, request):
        operation_id: int = request.GET.get("operation")

        key: int = operation_id
        response = cache.get(key)

        if response is None:
            response: Dict[str, Any] = OrderServices.get_order_by_details(operation_id)
            cache.set(key, response, timeout=120)

        return JsonResponse(data=response, status=status.HTTP_200_OK)
