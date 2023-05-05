from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet
from src.Core.paginators import OrderViewPaginnator

from src.MsSqlConnector.connector import connector as connector_service
from src.OrderView.models import IndexOperations
from src.OrderView.serializers import (
    DatabaseConnectionSerializer,
    DeleteConnectionSerializer,
    IndexStanowiskoSerializer,
    OperationNameSerializer,
    OrderDataByZlecenieSerializer,
    ProductSerializer,
)
from src.OrderView.services.operation_service import operation_service
from src.OrderView.services.order_list_service import order_list_service
from src.OrderView.services.order_service import order_service

from src.MsSqlConnector.connector import connector


class GetAllProductAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderViewPaginnator
    serializer_class = ProductSerializer

    @connector_service.check_database_connection
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
    @connector_service.check_database_connection
    def get(self, request, zlecenie_id):
        response = order_service.get_order(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)


class OperationNameApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OperationNameSerializer

    @method_decorator(cache_page(30))
    @connector_service.check_database_connection
    def get(self, request):
        response = operation_service.get_operation_names()
        return Response(response, status=status.HTTP_200_OK)


# TODO: Replace views below to Connector application
class CreateDatabaseConnectionAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DatabaseConnectionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if connector.is_stable(serializer.validated_data):
            serializer.save()
            connection = serializer.validated_data
            return Response(
                {
                    "success": True,
                    "message": "Database connection was created successfully",
                    "connection": DatabaseConnectionSerializer(connection).data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Database connection was not created successfully",
                    "connection": DatabaseConnectionSerializer(connection).data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteConectionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteConnectionSerializer

    def post(self, request, id):
        connector_service.delete_connection(id)
        return Response(
            {"success": True, "message": "Database was successfully deleted"},
            status=status.HTTP_200_OK,
        )


class GetDatabasesAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = connector_service.get_conections()
    serializer_class = DatabaseConnectionSerializer


class IndexOperationsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IndexOperations.objects.all()
    serializer_class = IndexStanowiskoSerializer
