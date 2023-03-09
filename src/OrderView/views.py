from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.serializers import ZleceniaSerializer


from src.OrderView.services import order_service


class GetAllDataAPIView(generics.ListAPIView):
    serializer_class = ZleceniaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return order_service.get_data()
