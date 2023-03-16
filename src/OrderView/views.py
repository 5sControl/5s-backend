from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from src.OrderView.serializers import ZleceniaSerializer, ZleceniaTestSerializer

from src.OrderView.services import orderView_service


class GetAllProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print('Got request')
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
        print("GET ORDER: ", zlecenie_id)
        response = orderView_service.get_order(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)
    

class TestApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        zlecenia = orderView_service.get_zleceniaQuery()
        serializer = ZleceniaTestSerializer(zlecenia, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
