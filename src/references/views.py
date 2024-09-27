from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from src.DatabaseConnections.models import ConnectionInfo
from src.manifest_api.get_data import get_erp_products, get_erp_operations, get_erp_equipment, get_erp_employees
from src.odoo_api.service import odoo_get_data, edit_answer_from_odoo


def build_redirect_url(host, port, reference_type):
    """Function for generating a URL for redirection"""
    return f"http://{host}:{port}/api/{reference_type}/"


class ErpReferenceView(APIView):
    def get(self, request, reference_type):
        connector = ConnectionInfo.objects.get(is_active=True)
        if connector.erp_system == "5s_control":
            host = connector.host
            port = connector.port
            if not host or not port:
                return Response({"error": "Host or port not specified"}, status=500)

            url = build_redirect_url(host, port, reference_type)
            return redirect(url)

        elif connector.erp_system == "manifest":
            if reference_type == "product-categories":
                data, status_code = get_erp_products()
            elif reference_type == "operations":
                data, status_code = get_erp_operations()
            elif reference_type == "equipment":
                data, status_code = get_erp_equipment()
            elif reference_type == "employees":
                data, status_code = get_erp_employees()
            else:
                return Response([], status=400)
            return Response(data, status=status_code)

        elif connector.erp_system == "odoo":
            if reference_type == "product-categories":
                table_name = "product.product"
            elif reference_type == "operations":
                table_name = "mrp.workorder"
            elif reference_type == "equipment":
                table_name = "mrp.bom"
            elif reference_type == "employees":
                table_name = "mrp.workcenter"
            elif reference_type == "product-categories":
                table_name = "product.category"
            else:
                return Response([], status=400)

            data, status_code = odoo_get_data(table_name)
            return Response(data, status=status_code)

        else:
            return Response([], status=400)
