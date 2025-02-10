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


def get_playlist_camera(time_start, time_end, camera_ip):
    request_dat = {
        "timeStart": time_start,
        "timeEnd": time_end,
        "cameraIp": camera_ip
    }
    url = f"{ONVIF_SERVICE_URL}:3456/create_manifest/"
    try:
        response = requests.post(
            url=url,
            json=request_dat,
        )
        response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None
