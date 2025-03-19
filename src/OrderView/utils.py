from typing import Any, Dict
import requests
import time
import logging


from src.Core.const import SERVER_URL, ONVIF_SERVICE_URL

logger = logging.getLogger(__name__)


def get_skany_video_info(time: time, camera_ip: str) -> Dict[str, Any]:
    url = f"{ONVIF_SERVICE_URL}:3010/api/cam-stream/videos/availability?time={time}&cameraIp={camera_ip}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error making request: {e}")
        return {"status": False}

    result: Dict[str, Any] = response.json()
    result["camera_ip"]: str = camera_ip
    result["status"] = True
    print("video result: ", result)
    return result


def get_playlist_camera(time_start, time_end, camera_ip, timespan_id):
    request_dat = {
        "timeStart": time_start,
        "timeEnd": time_end,
        "cameraIp": camera_ip,
        "timespanId": f"{timespan_id}"
    }
    url = f"{ONVIF_SERVICE_URL}:3010/api/cam-stream/videos/create-manifest/"
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
