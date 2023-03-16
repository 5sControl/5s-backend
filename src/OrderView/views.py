from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.services import orderView_service


class GetAllProductAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.get_filtered_orders_list()
        return Response(response, status=status.HTTP_200_OK)


class GetOrderDataByindexAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, index):
        response = orderView_service.get_productDataById(index)
        return Response(response, status=status.HTTP_200_OK)


class GetOrderDataByZlecenieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, zlecenie_id):
        response = orderView_service.get_order(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)


class TestAPIView(APIView):
    def get(self, request, zlecenie_id):
        response = orderView_service.test(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)
