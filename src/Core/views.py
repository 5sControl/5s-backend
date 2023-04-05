from rest_framework.response import Response
from rest_framework import status, generics

from src.Core.utils import send_request_to_update_service


class StartDeployment(generics.GenericAPIView):

    def post(self, request):
        service = request.GET.get("service")
        return Response(send_request_to_update_service(service), status=status.HTTP_102_PROCESSING)
