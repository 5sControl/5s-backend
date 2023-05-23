import os
import requests

from rest_framework.response import Response
from rest_framework import status, generics, viewsets, mixins

from .const import SERVER_URL
from .serializers import SystemMessagesSerializer
from .models import SystemMessage
from .paginators import SystemMessagesPaginator


class CheckMemoryStatus(generics.GenericAPIView):
    def get(self, request):
        usage_stats = os.statvfs(os.getcwd())

        block_size = usage_stats.f_frsize
        available_blocks = usage_stats.f_bavail
        available_space_gb = available_blocks * block_size / (1000**3)

        has_enough_space = available_space_gb > 15

        return Response({"has_enough_space": has_enough_space})


class FindCameraAPIView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        cameras_response = requests.get(f"{SERVER_URL}:7654/get_all_onvif_cameras/")
        try:
            cameras = cameras_response.json()
        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response_data = {"results": cameras}
        return Response(response_data, status=status.HTTP_200_OK)


class SystemMessagesApiView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = SystemMessagesSerializer
    queryset = SystemMessage.objects.all()
    pagination_class = SystemMessagesPaginator
