from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from src.OrderView.serializers import ZleceniaSerializer


import json

from src.OrderView.services import order_service


class GetAllDataListAPIView(generics.ListAPIView):
    serializer_class = ZleceniaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return order_service.get_data()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)