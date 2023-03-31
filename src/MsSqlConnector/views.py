from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from src.MsSqlConnector.services import create_records


class CreateSkanyAPIView(generics.GenericAPIView):
    def post(self, request):
        response = create_records.create_skany(
            request.data["beverage"], request.data["worker"]
        )
        if response:
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {"success": False, "message": "Cannot create skany record"},
            status=status.HTTP_400_BAD_REQUEST,
        )
