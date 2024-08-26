from typing import Any, Dict
import requests
import time
import logging


from src.Core.const import SERVER_URL, ONVIF_SERVICE_URL

logger = logging.getLogger(__name__)


def get_skany_video_info(time: time, camera_ip: str) -> Dict[str, Any]:
    request_data: Dict[str, Any] = {
        "camera_ip": camera_ip,
        "time": time,
    }
    print("request data for video: ", request_data)
    url = f"{ONVIF_SERVICE_URL}:3456/is_video_available/"
    # try:
    response: requests = requests.post(
        url=f"{url}",
        json=request_data,
    )
    print(response)
    # except Exception:
    #     return {"status": False}

    result: Dict[str, Any] = response.json()
    print("video result: ", result)
    result["camera_ip"]: str = camera_ip

    return result


def get_package_video_info(time: time, camera_ip: str) -> Dict[str, Any]:
    request_data: Dict[str, Any] = {
        "camera_ip": camera_ip,
        "time": time,
    }
    url = f"{ONVIF_SERVICE_URL}:3456/is_video_available/"
    try:
        response: requests = requests.post(
            url=f"{url}",
            json=request_data,
        )
    except Exception:
        return {"status": False}

    result: Dict[str, Any] = response.json()
    logger.warning(f"Video result: ", result)
    result["camera_ip"]: str = camera_ip

    return result
