import requests
import logging

from src.Core.const import SERVER_URL, ALGORITHMS_CONTROLLER_SERVICE_URL, ONVIF_SERVICE_URL

logger = logging.getLogger(__name__)


def sender(operation, data, cstm_port=None):
    url = None
    port = None

    if ALGORITHMS_CONTROLLER_SERVICE_URL:
        service_url = ALGORITHMS_CONTROLLER_SERVICE_URL
    else:
        service_url = SERVER_URL

    if operation == "add_camera":
        url = "/api/cam-stream/cameras"
        port = 3010
    elif operation == "run":
        url = "/run"
        port = 3333
    elif operation == "stop":
        url = "/stop"
        port = 3333
    elif operation == "search":
        url = f"/image/search?image_name={data}"
        port = 3333
    elif operation == "loading":
        url = f"/image/download?image_name={data}"
        port = 3333
    else:
        logger.error(f"Unknown operation: {operation}")
        return {"error": "Unknown operation"}

    if ALGORITHMS_CONTROLLER_SERVICE_URL and port == 3333:
        service_url = ALGORITHMS_CONTROLLER_SERVICE_URL

    if ONVIF_SERVICE_URL and port == 3010:
        service_url = ONVIF_SERVICE_URL

    if cstm_port:
        link = f"{service_url}:{cstm_port}{url}"
    else:
        link = f"{service_url}:{port}{url}"

    logger.warning(f"Sending request to {link} with data {data}")

    try:
        if operation in ["search", "loading"]:
            request = requests.get(link)
        else:
            request = requests.post(link, json=data)

        logger.warning(f"Request status from sender -> {request.status_code}")
        request.raise_for_status()

        result = request.json()
        logger.warning(f"Result from sender -> {result}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return {"error": str(e)}
