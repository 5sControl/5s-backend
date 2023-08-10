from typing import Any, Dict, List, Optional

import requests

from src.DatabaseConnections.models import ConnectionInfo


class OdooConnector:
    def get_operations(self, f_date: str, t_date: str) -> Optional[List[Dict[str, Any]]]:
        base_url: str = self._modify_url_by_path(self._get_base_url(), "operations")
        request_url: str = self._collect_query_params(base_url, f_date, t_date)

        response: List[Dict[str, Any]] = self._send_request(request_url)

        return response

    def get_orders(self, f_date: str, t_date: str) -> Optional[List[Dict[str, Any]]]:
        base_url: str = self._modify_url_by_path(self._get_base_url(), "orders")
        request_url: str = self._collect_query_params(base_url, f_date, t_date)

        response: List[Dict[str, Any]] = self._send_request(request_url)

        return response

    def _get_base_url(self, raise_exception: bool = True) -> str:
        if raise_exception:
            url: str = ConnectionInfo.objects.get(type="api", is_active=True).host
        else:
            url: str = ConnectionInfo.objects.filter(type="api", is_active=True).first().host

        return url + "/fives"

    def _send_request(self, url: str) -> List[Dict[str, Any]]:
        response: List[Dict[str, Any]] = requests.get(url)
        print(url)
        print(response.json())
        return self._serialize(response)

    def _collect_query_params(self, url: str, f_date: str, t_date: str) -> str:
        return f"{url}?from={f_date}&to={t_date}"

    def _modify_url_by_path(self, url: str, path: str) -> str:
        return f"{url}/{path}"

    def _serialize(self, response: requests.Response) -> List[Dict[str, Any]]:
        return response.json()


connector_services: OdooConnector = OdooConnector()
