import requests
import logging

from src.Core.const import SERVER_URL, ALGORITHMS_CONTROLLER_SERVICE_URL, ONVIF_SERVICE_URL

logger = logging.getLogger(__name__)


def Sender(operation, data, cstm_port=None):
    url = None
    port = None

    if ALGORITHMS_CONTROLLER_SERVICE_URL:
        service_url = ALGORITHMS_CONTROLLER_SERVICE_URL
    else:
        service_url = SERVER_URL

    if operation == "add_camera":
        url = "/add_camera"
        port = 3456
    if operation == "run":
        url = "/run"
        port = 3333
        # data["server_url"] = service_url

    if operation == "stop":
        url = "/stop"
        port = 3333

    if operation == "search":
        url = f"/image/search?image_name={data}"
        port = 3333

    if operation == "loading":
        url = f"/image/download?image_name={data}"
        port = 3333


    if ALGORITHMS_CONTROLLER_SERVICE_URL and port == 3333:
        service_url = ALGORITHMS_CONTROLLER_SERVICE_URL


    if ONVIF_SERVICE_URL and port == 3456:
        service_url = ONVIF_SERVICE_URL

    if cstm_port:
        link = f"{service_url}:{cstm_port}{url}"
    else:
        link = f"{service_url}:{port}{url}"

    if operation in ["search", "loading"]:
        request = requests.get(f"{service_url}:{port}{url}")
        logger.warning(f"Request status from sender docker_image -> {request}")
    else:
        request = requests.post(link, json=data)
        logger.warning(f"request status from sender -> {request}")
        request.raise_for_status()

    result = request.json()
    logger.warning(f"result from sender -> {result}")

    return result
