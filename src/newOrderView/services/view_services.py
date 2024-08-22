from typing import Any, Dict, List

from django.shortcuts import get_object_or_404
from django.core.cache import cache

from src.DatabaseConnections.models import ConnectionInfo
from src.manifest_api.sender import get_all_works_manifest
from src.manifest_api.service import get_all_reports_manifest
from src.newOrderView.services.connector import connector_services
from src.newOrderView.services.operations import OperationServices
from src.newOrderView.services.order import OrderServices


def get_response(
    cache_key: str,
    from_date: str,
    to_date: str,
    operation_type_ids: List[id],
    type: str,
) -> List[Dict[str, Any]]:
    connector = get_object_or_404(ConnectionInfo, is_active=True).type
    response = []

    if connector == "api":
        if type == "operation":
            response_manifest = None
            try:
                if ConnectionInfo.objects.get(is_active=True, erp_system="manifest"):
                    response_manifest = get_all_works_manifest(from_date, to_date)
            except Exception as e:
                response_manifest = []
                print(f"Exception operation response manifest: {e}")

            try:
                response_winkhaus: List[Dict[str, Any]] = connector_services.get_operations(
                    from_date, to_date
                )
            except Exception as e:
                print(f"Exception operation: {e}")
                response_winkhaus = []

            response = response_manifest + response_winkhaus

        elif type == "orders":
            if ConnectionInfo.objects.filter(is_active=True, erp_system="manifest"):
                result = get_all_works_manifest(from_date, to_date)
                return result
            else:
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

    return response
