from rest_framework.response import Response
from rest_framework.views import APIView
from src.DatabaseConnections.models import ConnectionInfo
from src.DatabaseConnections.services import get_data_five_control
from src.manifest_api.get_data import get_erp_products, get_erp_operations, get_erp_equipment, get_erp_employees


class ErpReferenceProductsView(APIView):
    def get(self, request):
        if ConnectionInfo.objects.filter(is_active=True, erp_system="manifest").exists():
            data, status_code = get_erp_products()
            return Response(data, status=status_code)
        elif not ConnectionInfo.objects.filter(is_active=True):
            data, status_code = get_data_five_control("products")
            return Response(data, status=status_code)
        else:
            return Response([], status=400)


class ReferenceOperationsView(APIView):
    def get(self, request):
        if ConnectionInfo.objects.filter(is_active=True, erp_system="manifest").exists():
            data, status_code = get_erp_operations()
            return Response(data, status=status_code)
        elif not ConnectionInfo.objects.filter(is_active=True):
            data, status_code = get_data_five_control("operations")
            return Response(data, status=status_code)
        else:
            return Response([], status=400)


class ReferenceEquipmentView(APIView):
    def get(self, request):
        if ConnectionInfo.objects.filter(is_active=True, erp_system="manifest").exists():
            data, status_code = get_erp_equipment()
            return Response(data, status=status_code)
        elif not ConnectionInfo.objects.filter(is_active=True):
            data, status_code = get_data_five_control("equipment")
            return Response(data, status=status_code)
        else:
            return Response([], status=400)


class ReferenceEmployeesView(APIView):
    def get(self, request):
        if ConnectionInfo.objects.filter(is_active=True, erp_system="manifest").exists():
            data, status_code = get_erp_employees()
            return Response(data, status=status_code)
        elif not ConnectionInfo.objects.filter(is_active=True):
            data, status_code = get_data_five_control("employees")
            return Response(data, status=status_code)
        else:
            return Response([], status=400)
