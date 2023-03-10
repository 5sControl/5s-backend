from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.services import orderView_service


class GetAllDataAPIView(APIView):
    # If you have a lot of time u can run it

    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.getAllData()
        return Response(response, status=status.HTTP_200_OK)


class GetAllOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.getAllOrders()
        return Response(response, status=status.HTTP_200_OK)


class GetOrderDataByIdAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, zlecenie_id):
        response = orderView_service.getOrderDataById(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)
