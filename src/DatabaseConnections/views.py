import requests
import json

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from src.DatabaseConnections.models import ConnectionInfo
from src.DatabaseConnections.serilisers import ConnectionInfoSerializer


class ActiveResourceView(generics.GenericAPIView):
    serializer_class = ConnectionInfoSerializer

    def get(self, request, *args, **kwargs):
        active_source = ConnectionInfo.objects.filter(is_active=True)
        if active_source.exists():
            return Response(
                {"type": active_source.first().type}, status=status.HTTP_200_OK
            )
        return Response({"type": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        connector_type: str = request.data.get("type")

        if connector_type == "database":
            connector_to_activate: ConnectionInfo = ConnectionInfo.objects.filter(
                type="database"
            )
            connector_to_deactivate: ConnectionInfo = ConnectionInfo.objects.filter(
                type="api"
            )
        elif connector_type == "api":
            connector_to_activate: ConnectionInfo = ConnectionInfo.objects.filter(
                type="api"
            )
            connector_to_deactivate: ConnectionInfo = ConnectionInfo.objects.filter(
                type="database"
            )
        else:
            return Response(
                {"detail": "Either 'api' or 'database' parameter must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not connector_to_activate.exists():
            return Response(
                {"detail": "Connection doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        connector_to_deactivate.update(is_active=False)
        connector_to_activate.update(is_active=True)
        return Response({"detail": "Active resource updated successfully."})


class GetOdooAllItems(APIView):
    def get(self, request, *args, **kwargs):
        """Returns a list of all items from the ODOO"""
        try:
            connection = ConnectionInfo.objects.filter(type="api").values('host', 'database', 'username', 'password')[0]

            if connection['host'] is None:
                raise ValueError("Missing connection host")
            if connection['username'] is None:
                raise ValueError("Missing connection username")
            if connection['password'] is None:
                raise ValueError("Missing connection password")
            if connection['database'] is None:
                raise ValueError("Missing connection database")
            response = requests.get(f"{connection['host']}/min_max/all_items")
            if response.status_code == 200:
                data = response.json().get('data')
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to fetch data from external service"}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
