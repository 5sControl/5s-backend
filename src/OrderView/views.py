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


class GetAllOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.get_allProduct()
        return Response(response, status=status.HTTP_200_OK)


class GetOrderDataByIdAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, zlecenie_id):
        response = orderView_service.get_productDataById(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)


class GetOrderApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.get_order()
        return Response(response, status=status.HTTP_200_OK)
