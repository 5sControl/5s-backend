from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from src.OrderView.serializers import DatabaseConnectionSerializer, ProductSerializer
from src.OrderView.services import orderView_service, connector
from src.OrderView.utils import OrderViewPaginnator


class GetAllProductAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderViewPaginnator
    serializer_class = ProductSerializer

    def get(self, request):
        search = request.GET.get("search")
        response = orderView_service.get_order_list(search)
        paginated_items = self.paginate_queryset(response)
        serializer = self.serializer_class(paginated_items, many=True)
        return self.get_paginated_response(serializer.data)


class GetOrderDataByZlecenieAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, zlecenie_id):
        response = orderView_service.get_order(zlecenie_id)
        if response:
            return Response(response, status=status.HTTP_200_OK)
        return Response(
            {"success": False, "message": "Database connection error"},
            status=status.HTTP_403_FORBIDDEN,
        )


# TODO: Replace views below to Connector application
class CreateConectionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            connection = connector.create_connection(request.data)
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.detail["data"],
                },  # TODO: return message istead object
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
        connector.delete_connection(id)
        return Response(
            {"success": True, "message": "Database was successfully deleted"},
            status=status.HTTP_200_OK,
        )


class GetDatabasesAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = connector.get_conections()
    serializer_class = DatabaseConnectionSerializer
