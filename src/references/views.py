import requests

from rest_framework.response import Response
from rest_framework.views import APIView
from src.DatabaseConnections.models import ConnectionInfo
from src.manifest_api.get_data import get_erp_products, get_erp_operations, get_erp_equipment, get_erp_employees
from src.odoo_api.service import odoo_get_data, edit_answer_from_odoo
import logging

logger = logging.getLogger(__name__)


def proxy_request(request, url):
    """Function for proxying requests to a specified URL."""
    method = request.method
    print("method", method)
    headers = {
        'Content-Type': request.headers.get('Content-Type', 'application/json')
    }

    if url.endswith('/'):
        url = url.rstrip('/')

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=request.GET, allow_redirects=False)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=request.data, allow_redirects=False)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=request.data, allow_redirects=False)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, allow_redirects=False)
            print('Response DELETED:', response.status_code)
        else:
            return Response({"error": "Unsupported HTTP method"}, status=405)

        # Проверяем, есть ли редирект
        if response.status_code in [301, 302] and 'Location' in response.headers:
            redirect_url = response.headers['Location']
            print(f"Redirecting to {redirect_url} with method {method}")
            # Повторяем запрос с сохранением метода
            if method == 'GET':
                response = requests.get(redirect_url, headers=headers, params=request.GET)
            elif method == 'POST':
                response = requests.post(redirect_url, headers=headers, json=request.data)
            elif method == 'PATCH':
                response = requests.patch(redirect_url, headers=headers, json=request.data)
            elif method == 'DELETE':
                response = requests.delete(redirect_url, headers=headers)

        return Response(response.json(), status=response.status_code)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error when proxying request:{e}")
        return Response({"error": "Error connecting to external service"}, status=500)

def build_redirect_url(host, port, reference_type):
    """Function to generate URL for redirection."""
    return f"{host}:{port}/{reference_type}"


class ErpReferenceView(APIView):
    def get(self, request, reference_type):
        return self.handle_request(request, reference_type)

    def post(self, request, reference_type):
        return self.handle_request(request, reference_type)

    def put(self, request, reference_type):
        return self.handle_request(request, reference_type)

    def delete(self, request, reference_type):
        return self.handle_request(request, reference_type)

    def handle_request(self, request, reference_type):
        if not reference_type:
            return Response({"error": "reference_type is required"}, status=400)
        connector = ConnectionInfo.objects.get(is_active=True)

        if connector.erp_system == "5s_control":
            host = connector.host
            port = connector.port

            if not host or not port:
                logger.error("Host or port not specified for 5s_control system")
                return Response({"error": "Host or port not specified"}, status=500)

            url = build_redirect_url(host, port, reference_type)
            print(f"Proxying a request to {url}")

            return proxy_request(request, url)

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
