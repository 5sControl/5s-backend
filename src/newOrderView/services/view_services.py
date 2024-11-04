from typing import Any, Dict, List

from django.shortcuts import get_object_or_404
from django.core.cache import cache

from src.DatabaseConnections.models import ConnectionInfo
from src.Reports.service import get_reports_orders_5s
from src.manifest_api.sender import get_all_works_manifest
from src.newOrderView.services.connector import connector_services
from src.newOrderView.services.operations import OperationServices
from src.newOrderView.services.order import OrderServices
from src.odoo_api.service import get_all_order_odoo, sorted_data_odoo


def get_response(
    cache_key: str,
    from_date: str,
    to_date: str,
    operation_type_ids: List[id],
    type: str,
) -> List[Dict[str, Any]]:
    connector = get_object_or_404(ConnectionInfo, used_in_orders_view=True).type
    response = []
    connection = ConnectionInfo.objects.filter(used_in_orders_view=True).first()

    try:
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return cached_response
    except Exception as e:
        print(f"Redis cache get exception: {e}")

    if connector == "api":
        if type == "operation":
            response_manifest = []
            response_odoo = []
            response_5s = []

            try:
                if connection.erp_system == "manifest":
                    response_manifest = get_all_works_manifest(from_date, to_date)
            except Exception as e:
                print(f"Exception operation response manifest: {e}")

                # Retrieving data from Odoo
            if connection.erp_system == "odoo":
                try:
                    data_odoo = get_all_order_odoo(from_date, to_date)
                    response_odoo = sorted_data_odoo(data_odoo, type)
                except Exception as e:
                    print(f"Exception operation response odoo: {e}")
                    response_odoo = []

                # Receiving data from 5s_control
            if connection.erp_system == "5s_control":
                response_5s = get_reports_orders_5s(from_date, to_date, "operations")

               # Receiving data from Winkhaus
            try:
                response_winkhaus = connector_services.get_operations(from_date, to_date)
            except Exception as e:
                print(f"Exception operation: {e}")
                response_winkhaus = []

            response = response_manifest + response_winkhaus + response_odoo + response_5s

        elif type == "orders":
            if connection.erp_system == "manifest":
                result = get_all_works_manifest(from_date, to_date, "orders")
                if result is None:
                    return []
                return result

            if connection.erp_system == "odoo":
                data_odoo = get_all_order_odoo(from_date, to_date)
                odoo_result = sorted_data_odoo(data_odoo, "orders")
                return odoo_result

            if connection.erp_system == "5s_control":
                response_5s = get_reports_orders_5s(from_date, to_date, "orders")
                return response_5s

            if connection.erp_system == "winkhaus":
                try:
                    response: List[Dict[str, Any]] = connector_services.get_orders(
                        from_date, to_date
                    )
                except Exception as e:
                    print(f"Exception orders: {e}")
                    response = []

    elif connector == "database":
        try:
            response = cache.get(cache_key)
        except Exception as e:
            print(f"Redis cash exception: {e}")
        if response is None:
            if type == "operation":
                response: List[Dict[str, Any]] = OperationServices.get_operations(
                    from_date, to_date, operation_type_ids
                )
            elif type == "orders":
                response: List[Dict[str, Any]] = OrderServices.get_order(
                    from_date, to_date, operation_type_ids
                )

            cache.set(cache_key, response, timeout=120)

    if response:
        try:
            cache.set(cache_key, response, timeout=120)  # Кэшируем на 120 секунд
        except Exception as e:
            print(f"Redis cache set exception: {e}")

    return response
