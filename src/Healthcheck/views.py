from typing import Any, Dict
from rest_framework import generics, status
from rest_framework.response import Response

from src.Core.paginators import NoPagination

from .serializers import CpuLoadSerializer
from .utils import get_healthckeck_data


class GetHealthCheckApiView(generics.GenericAPIView):
    pagination_class = NoPagination
    serializer_class = CpuLoadSerializer

    def get(self, request):
        result: Dict[str, Any] = get_healthckeck_data()
        return Response(result, status=status.HTTP_200_OK)
