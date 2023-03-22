from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from src.OrderView.models import DatabaseConnection
from src.OrderView.serializers import DatabaseConnectionSerializer
from src.OrderView.services import orderView_service, ms_sql_service


class GetAllProductAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.get_filtered_orders_list()
        return Response(response, status=status.HTTP_200_OK)


class GetOrderDataByZlecenieAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, zlecenie_id):
        response = orderView_service.get_order(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)


class CreateConectionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            id = ms_sql_service.create_connection(request.data)
        except ValidationError as e:
            return Response(
                {"success": False, "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"success": True, "message": "Database was successfully", "id": id},
            status=status.HTTP_201_CREATED,
        )


class DeleteConectionAPIView(generics.RetrieveDestroyAPIView):
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer
    lookup_field = 'id'


class DeleteConectionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        ms_sql_service.delete_connection(id)
        return Response(
            {},
            status=status.HTTP_204_NO_CONTENT,
        )


class GetDatabasesAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ms_sql_service.get_conections()
    serializer_class = DatabaseConnectionSerializer
