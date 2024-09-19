from rest_framework.response import Response
from rest_framework.views import APIView
from src.DatabaseConnections.models import ConnectionInfo
from src.manifest_api.get_data import get_erp_products


class ConnectionErpReferenceView(APIView):
    def get(self, request):
        if ConnectionInfo.objects.filter(is_active=True, erp_system="manifest").exists():
            data, status_code = get_erp_products()
            return Response(data, status=status_code)
        else:
            return Response([], status=400)
