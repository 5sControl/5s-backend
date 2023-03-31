from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from src.OrderView.serializers import DatabaseConnectionSerializer, ProductSerializer
from src.OrderView.services import orderView_service
from src.OrderView.utils import OrderViewPaginnator

from src.MsSqlConnector.connector import connector as connector_service


class GetAllProductAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderViewPaginnator
    serializer_class = ProductSerializer

    @connector_service.check_database_connection
    def get(self, request):
        search = request.GET.get("search")
        status = request.GET.get("status")
        response = orderView_service.get_order_list(search=search, status=status)
        paginated_items = self.paginate_queryset(response)
        serializer = self.serializer_class(paginated_items, many=True)
        return self.get_paginated_response(serializer.data)


class GetOrderDataByZlecenieAPIView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]

    @connector_service.check_database_connection
    def get(self, request, zlecenie_id):
        response = orderView_service.get_order(zlecenie_id)
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
