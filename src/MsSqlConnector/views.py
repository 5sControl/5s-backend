from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from src.MsSqlConnector.services import create_records


class CreateSkanyAPIView(generics.GenericAPIView):
    def get(self, request):
        response = create_records.create_skany(request.data["beverage"])
        if response:
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {"success": False, "message": "Connot create skany record"},
            status=status.HTTP_400_BAD_REQUEST,
        )
