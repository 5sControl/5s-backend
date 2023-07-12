from typing import Dict, List, Any, Optional

from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework import generics, status
from rest_framework.response import Response

from src.Core.paginators import NoPagination
from src.DatabaseConnections.utils import check_database_connection
from src.newOrderView.models import FiltrationOperationsTypeID
from src.newOrderView.serializers import FilterOperationsTypeIDSerializer

from .services import OperationServices, OrderServices
from .utils import generate_hash


class GetOperation(generics.GenericAPIView):
    pagination_class = NoPagination

    @check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        operation_type_ids = FiltrationOperationsTypeID.objects.filter(
            is_active=True
        ).values_list("operation_type_id", flat=True)
        operation_type_ids = list(operation_type_ids)

        key: str = (
            generate_hash("get_operation", from_date, to_date)
            + ":"
            + ":".join(str(id) for id in operation_type_ids)
        )
        response = cache.get(key)

        if response is None:
            response: List[Dict[str, Any]] = OperationServices.get_operations(
                from_date, to_date, operation_type_ids
            )
            cache.set(key, response, timeout=120)

        if response:
            return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetMachine(generics.GenericAPIView):
    pagination_class = NoPagination

    @check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        operation_type_ids = FiltrationOperationsTypeID.objects.filter(
            is_active=True
        ).values_list("operation_type_id", flat=True)
        operation_type_ids = list(operation_type_ids)

        key: str = (
            generate_hash("get_machine", from_date, to_date)
            + ":"
            + ":".join(str(id) for id in operation_type_ids)
        )
        response = cache.get(key)

        if response is None:
            response: List[Dict[str, Any]] = OperationServices.get_machine(
                from_date, to_date, operation_type_ids
            )
            cache.set(key, response, timeout=60)

        if response:
            return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetOrders(generics.GenericAPIView):
    pagination_class = NoPagination

    @check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        operation_type_ids = FiltrationOperationsTypeID.objects.filter(
            is_active=True
        ).values_list("operation_type_id", flat=True)
        operation_type_ids = list(operation_type_ids)

        key: str = (
            generate_hash("get_order", from_date, to_date)
            + ":"
            + ":".join(str(id) for id in operation_type_ids)
        )
        response = cache.get(key)

        if response is None:
            response: List[Dict[str, str]] = OrderServices.get_order(
                from_date, to_date, operation_type_ids
            )
            cache.set(key, response, timeout=120)

        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


class GetOrderByDetail(generics.GenericAPIView):
    pagination_class = NoPagination

    @check_database_connection
    def get(self, request):
        operation_id: int = request.GET.get("operation")
        response: Dict[str, Any] = OperationServices.get_operation_by_details(
            operation_id
        )
        return JsonResponse(data=response, status=status.HTTP_200_OK)


class GetWhnetOperation(generics.GenericAPIView):
    pagination_class = NoPagination

    @method_decorator(cache_page(30))
    @check_database_connection
    def get(self, request):
        response: Dict[str, Any] = OperationServices.get_whnet_operation()
        return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)


class FiltrationsDataView(generics.ListAPIView):
    serializer_class = FilterOperationsTypeIDSerializer
    pagination_class = NoPagination
    queryset = FiltrationOperationsTypeID.objects.all()

    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            for item in data:
                instance = FiltrationOperationsTypeID.objects.get(pk=item["id"])
                serializer = self.get_serializer(instance, data=item, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return self.get_response(message="Status updated successfully.")
        except Exception as e:
            return self.get_response(error=str(e), status=400)

    def get_response(self, message=None, error=None, status=200):
        response_data = {}
        if message:
            response_data["message"] = message
        if error:
            response_data["error"] = error
        return Response(response_data, status=status)


class GetOperationsDuration(generics.GenericAPIView):
    pagination_class = NoPagination

    @check_database_connection
    def get(self, requests):
        ids: Optional[List[int]] = requests.GET.getlist("id")
        key: str = "get_duration" + str(ids)
        response: str = cache.get(key)

        if response is None:
            response: List[Dict[str, str]] = OperationServices.calculate_avg_duration(
                ids
            )
            cache.set(key, response, timeout=360)

        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)
