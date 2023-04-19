import os

from rest_framework.response import Response
from rest_framework import status, generics

from src.Core.utils import send_request_to_update_service


class StartDeployment(generics.GenericAPIView):

    def post(self, request):
        print("Starting deployment")
        service = request.GET.get("service")
        return Response(send_request_to_update_service(service), status=status.HTTP_102_PROCESSING)


class CheckMemoryStatus(generics.GenericAPIView):
    def get(self, request):
        usage_stats = os.statvfs(os.getcwd())

        block_size = usage_stats.f_frsize
        available_blocks = usage_stats.f_bavail
        available_space_gb = available_blocks * block_size / (1000 ** 3)

        has_enough_space = available_space_gb > 15

        return Response({'has_enough_space': has_enough_space})
