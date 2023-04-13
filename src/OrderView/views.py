from django.views.decorators.cache import cache_page

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet

from src.MsSqlConnector.connector import connector as connector_service
from src.OrderView.models import IndexOperations
from src.OrderView.serializers import (
    DatabaseConnectionSerializer, IndexStanowiskoSerializer, ProductSerializer
)
from src.OrderView.services.operation_service import operation_service
from src.OrderView.services.order_list_service import order_list_service
from src.OrderView.services.order_service import order_service

from src.OrderView.utils import OrderViewPaginnator


class GetAllProductAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderViewPaginnator
    serializer_class = ProductSerializer

    @connector_service.check_database_connection
    @cache_page(10, key_prefix='order_list_view')
    def get(self, request):
        from_time = request.GET.get("from")
        to_time = request.GET.get("to")
        search = request.GET.get("search")
        order_status = request.GET.get("order-status")
        operation_status = request.GET.getlist("operation-status")
        operation_name = request.GET.getlist("operation-name")

        response = order_list_service.get_order_list(
            search=search,
            order_status=order_status,
            operation_status=operation_status,
            operation_name=operation_name,
            from_time=from_time,
            to_time=to_time,
        )

        paginated_items = self.paginate_queryset(response)
        serializer = self.serializer_class(paginated_items, many=True)

        return self.get_paginated_response(serializer.data)


class GetOrderDataByZlecenieAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @connector_service.check_database_connection
    @cache_page(10)
    def get(self, request, zlecenie_id):
        response = order_service.get_order(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)


class OperationNameApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @connector_service.check_database_connection
    @cache_page(30)
    def get(self, request):
        response = operation_service.get_operation_names()
        return Response(response, status=status.HTTP_200_OK)


# TODO: Replace views below to Connector application
class CreateConectionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            connection = connector_service.create_connection(request.data)
        except ValidationError as e:
            error_detail = str(e.detail.get("detail", ""))
            return Response(
                {
                    "success": False,
                    "message": error_detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "success": True,
                "message": "Database was successfully",
                "connection": connection,
            },
            status=status.HTTP_201_CREATED,
        )


class DeleteConectionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

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
