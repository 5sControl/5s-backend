from typing import Dict, List, Any, Optional

from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.Core.paginators import NoPagination
from src.DatabaseConnections.utils import check_database_connection
from src.newOrderView.models import FiltrationOperationsTypeID
from src.newOrderView.repositories.order import OrderRepository
from src.newOrderView.serializers import FilterOperationsTypeIDSerializer

from .services import OperationServices
from .services.view_services import get_response
from .utils import get_cache_data, get_date_interval, find_camera_by_workspace
from ..OrderView.utils import get_package_video_info


class GetOperation(generics.GenericAPIView):
    pagination_class = NoPagination

    @check_database_connection
    def get(self, request):
        from_date, to_date = get_date_interval(request)
        cache_key, operation_type_ids = get_cache_data('get_operation', from_date, to_date)

        response: List[Dict[str, Any]] = get_response(
            cache_key, from_date, to_date, operation_type_ids, "operation"
        )

        return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)


class GetOrders(generics.GenericAPIView):
    pagination_class = NoPagination

    @check_database_connection
    def get(self, request):
        from_date, to_date = get_date_interval(request)
        cache_key, operation_type_ids = get_cache_data('get_order', from_date, to_date)

        response: List[Dict[str, Any]] = get_response(
            cache_key, from_date, to_date, operation_type_ids, "orders"
        )

        return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)


class GetMachine(generics.GenericAPIView):
    pagination_class = NoPagination

    @check_database_connection
    def get(self, request):
        from_date, to_date = get_date_interval(request)
        cache_key, operation_type_ids = get_cache_data('get_machine', from_date, to_date)

        response = cache.get(cache_key)

        if response is None:
            response: List[Dict[str, Any]] = OperationServices.get_machine(
                from_date, to_date, operation_type_ids
            )
            cache.set(cache_key, response, timeout=60)

        if response:
            return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class GetOrderPackaging(APIView):
    pagination_class = NoPagination
    order_repository = OrderRepository()

    @check_database_connection
    def get(self, requests):
        result = []
        order_number = requests.GET.get("order_number")
        camera = find_camera_by_workspace()
        operation_times = self.order_repository.packing_time_search(order_number)

        if not operation_times:
            return Response(
                {"message": f"No video found for order {order_number}"},
                status=status.HTTP_404_NOT_FOUND
            )

        for operation_time in operation_times:
            video_info = get_package_video_info(operation_time, camera)

            if video_info.get("status"):
                result.append(video_info)

        return Response(result)




