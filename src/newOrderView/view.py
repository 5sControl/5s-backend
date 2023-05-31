from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics

from src.MsSqlConnector.connector import connector as connector_service
from src.OrderView.serializers import (
    OperationNameSerializer,
)
from src.OrderView.services.operation_service import operation_service


class OperationNameApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OperationNameSerializer

    @method_decorator(cache_page(30))
    @connector_service.check_database_connection
    def get(self, request):
        response = operation_service.get_operation_names()
        return Response(response, status=status.HTTP_200_OK)


