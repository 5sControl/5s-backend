from rest_framework.response import Response
from rest_framework.views import APIView
from src.DatabaseConnections.models import ConnectionInfo
from src.DatabaseConnections.services import get_data_five_control
from src.manifest_api.get_data import get_erp_products, get_erp_operations, get_erp_equipment, get_erp_employees
from src.odoo_api.service import odoo_get_data, edit_answer_from_odoo


class ErpReferenceProductsView(APIView):
    def get(self, request):
        connector = ConnectionInfo.objects.get(is_active=True)
        if connector.erp_system == "manifest":
            data, status_code = get_erp_products()
            return Response(data, status=status_code)

        elif connector.erp_system == "odoo":
            table_name = "product.product"
            data, status_code = odoo_get_data(table_name)
            return Response(data, status=status_code)

        elif connector.erp_system == "5s_control":
            data, status_code = get_data_five_control("products")
            return Response(data, status=status_code)
        else:
            return Response([], status=400)


class ReferenceOperationsView(APIView):
    def get(self, request):
        connector = ConnectionInfo.objects.get(is_active=True)
        if connector.erp_system == "manifest":
            data, status_code = get_erp_operations()
            return Response(data, status=status_code)

        elif connector.erp_system == "odoo":
            table_name = "mrp.workorder"
            data, status_code = odoo_get_data(table_name)
            return Response(data, status=status_code)

        elif connector.erp_system == "5s_control":
            data, status_code = get_data_five_control("operations")
            return Response(data, status=status_code)
        else:
            return Response([], status=400)


class ReferenceEquipmentView(APIView):
    def get(self, request):
        connector = ConnectionInfo.objects.get(is_active=True)
        if connector.erp_system == "manifest":
            data, status_code = get_erp_equipment()
            return Response(data, status=status_code)

        elif connector.erp_system == "odoo":
            table_name = "mrp.bom"
            fields = ["id", "display_name"]
            data, status_code = odoo_get_data(table_name, fields)
            result = edit_answer_from_odoo(data)
            return Response(result, status=status_code)

        elif connector.erp_system == "5s_control":
            data, status_code = get_data_five_control("equipment")
            return Response(data, status=status_code)
        else:
            return Response([], status=400)


class ReferenceEmployeesView(APIView):
    def get(self, request):
        connector = ConnectionInfo.objects.get(is_active=True)
        if connector.erp_system == "manifest":
            data, status_code = get_erp_employees()
            return Response(data, status=status_code)

        elif connector.erp_system == "odoo":
            table_name = "mrp.workcenter"
            data, status_code = odoo_get_data(table_name)
            return Response(data, status=status_code)

        elif connector.erp_system == "5s_control":
            data, status_code = get_data_five_control("employees")
            return Response(data, status=status_code)
        else:
            return Response([], status=400)
