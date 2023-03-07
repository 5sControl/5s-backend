from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.serializers import ZleceniaSerializer


import json

from src.OrderView.services import order_service


class GetAllDataAPIView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        results = order_service.get_data()
        serialized_results = json.dumps(results, default=order_service.datetime_to_str)
        return Response(serialized_results, content_type='application/json')
