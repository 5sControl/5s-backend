from typing import Any, Dict, List

from django.shortcuts import get_object_or_404
from django.core.cache import cache

from src.DatabaseConnections.models import ConnectionInfo
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

    if connector == "api":
        if type == "operation":
            response: List[Dict[str, Any]] = connector_services.get_operations(
                from_date, to_date
            )
        elif type == "orders":
            response: List[Dict[str, Any]] = connector_services.get_orders(
                from_date, to_date
            )
    elif connector == "database":
        response = cache.get(cache_key)
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
