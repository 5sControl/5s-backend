from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.services import orderView_service


class GetAllDataAPIView(APIView):
    # If you have a lot of time u can run it

    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.get_all()
        return Response(response, status=status.HTTP_200_OK)


class GetAllProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.get_allProduct()
        return Response(response, status=status.HTTP_200_OK)


class GetOrderDataByindexAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, index):
        response = orderView_service.get_productDataById(index)
        return Response(response, status=status.HTTP_200_OK)


class GetOrderDataByZlecenieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, zlecenie):
        response = orderView_service.get_order(zlecenie)
        return Response(response, status=status.HTTP_200_OK)
