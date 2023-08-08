from rest_framework.response import Response
from rest_framework import generics, status

from src.DatabaseConnections.models import ConnectionInfo
from src.DatabaseConnections.serilisers import ConnectionInfoSerializer


class UpdateActiveResourceView(generics.UpdateAPIView):
    serializer_class = ConnectionInfoSerializer

    def update(self, request, *args, **kwargs):
        connector_type: str = request.data.get("type")

        if connector_type == "database":
            connector: ConnectionInfo = ConnectionInfo.objects.filter(type="database")
            if not connector.exists():
                return Response({"detail": "Connection doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            connector.update(is_active=True)
        elif connector_type == "api":
            connector: ConnectionInfo = ConnectionInfo.objects.filter(type="api")
            if not connector.exists():
                return Response({"detail": "Connection doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            connector.update(is_active=True)
        else:
            return Response(
                {"detail": "Either 'api' or 'database' parameter must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": "Active resource updated successfully."})
