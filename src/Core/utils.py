import requests
import logging

from src.Core.const import SERVER_URL

logger = logging.getLogger(__name__)


def Sender(operation, data, cstm_port=None):
    url = None
    port = None

    if operation == "add_camera":
        url = "/add_camera"
        port = 3456
    if operation == "run":
        url = "/run"
        port = 3333
        data["server_url"] = SERVER_URL

    if operation == "stop":
        url = "/stop"
        port = 3333

    if cstm_port:
        link = f"{SERVER_URL}:{cstm_port}{url}"
    else:
        link = f"{SERVER_URL}:{port}{url}"

    request = requests.post(link, json=data)
    print(111111111, request.content)
    logger.warning(f"request status from sender -> {request}")
    request.raise_for_status()

    result = request.json()
    logger.warning(f"result from sender -> {result}")

    return result
