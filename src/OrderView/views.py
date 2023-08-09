from typing import Any, Dict, Tuple, Type, Callable
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from src.DatabaseConnections.models import ConnectionInfo
from src.DatabaseConnections.serilisers import ConnectorStatusSerializer

from src.DatabaseConnections.services import (
    CreateConnectionManager,
)
from src.Core.paginators import OrderViewPaginnator
from src.DatabaseConnections.utils import check_database_connection
from src.OrderView.models import IndexOperations
from src.OrderView.serializers import (
    ApiConnectionSerializer,
    DatabaseConnectionSerializer,
    DeleteConnectionSerializer,
    IndexStanowiskoSerializer,
    OperationNameSerializer,
    OrderDataByZlecenieSerializer,
    ProductSerializer,
)
from src.OrderView.services.order_list_service import order_list_service
from src.OrderView.services.order_service import order_service
from src.newOrderView.repositories.stanowisko import WorkplaceRepository


class GetAllProductAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderViewPaginnator
    serializer_class = ProductSerializer

    @check_database_connection
    def get(self, request):
        from_time = request.GET.get("from")
        to_time = request.GET.get("to")
        search = request.GET.get("search")
        order_status = request.GET.get("order-status")
        operation_status = request.GET.getlist("operation-status")
        operation_name = request.GET.getlist("operation-name")

        cache_key = f"all_products_{search}_{order_status}_{operation_status}_{operation_name}_{from_time}_{to_time}"

        response = cache.get(cache_key)

        if response is None:
            response = order_list_service.get_order_list(
                search=search,
                order_status=order_status,
                operation_status=operation_status,
                operation_name=operation_name,
                from_time=from_time,
                to_time=to_time,
            )

            cache.set(cache_key, response, timeout=120)

        paginated_items = self.paginate_queryset(response)
        serializer = self.serializer_class(paginated_items, many=True)

        return self.get_paginated_response(serializer.data)


class GetOrderDataByZlecenieAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDataByZlecenieSerializer

    @method_decorator(cache_page(30))
    @check_database_connection
    def get(self, request, zlecenie_id):
        response = order_service.get_order(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)


class OperationNameApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OperationNameSerializer

    @method_decorator(cache_page(30))
    @check_database_connection
    def get(self, request):
        wokplace_repo: WorkplaceRepository = WorkplaceRepository()

        response = wokplace_repo.get_workplaces_names()
        return Response(response, status=status.HTTP_200_OK)


# TODO: Replace views below to Connector application
class CreateConnectionAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    CONNECTION_TYPE_MAPPING: Dict[str, Tuple[Type[serializers.ModelSerializer], Callable[[CreateConnectionManager, Dict[str, Any]], bool]]] = {
        "api": (ApiConnectionSerializer, CreateConnectionManager.create_api_connection),
        "database": (DatabaseConnectionSerializer, CreateConnectionManager.create_database_connection),
    }

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        connection_type: str = request.data.get("type")

        serializer_class, manager_method = self.CONNECTION_TYPE_MAPPING.get(connection_type, (None, None))

        if not serializer_class or not manager_method:
            return Response(
                {"success": False, "message": "Invalid connection type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer: serializers.ModelSerializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        credentials: Dict[str, Any] = serializer.validated_data

        manager: CreateConnectionManager = CreateConnectionManager()
        result: bool = manager_method(manager, credentials)

        if result:
            return Response(
                {"status": True, "message": "Connection was successfully created"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": False, "message": "Connection was not created"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteConectionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteConnectionSerializer

    def post(self, request, id):
        manager: CreateConnectionManager = CreateConnectionManager()

        if manager.delete_connection(id):
            return Response(
                {"success": True, "message": "Connection was successfully deleted"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "message": "Connection ID does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetConnectionStatusAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectorStatusSerializer

    def get_object(self):
        db_connection = ConnectionInfo.objects.filter(type="database").first()
        api_connection = ConnectionInfo.objects.filter(type="api").first()
        return {"db": db_connection, "api": api_connection}


class IndexOperationsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IndexOperations.objects.all()
    serializer_class = IndexStanowiskoSerializer
