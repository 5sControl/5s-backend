from typing import Any, Dict
import requests
import time

from src.Core.const import SERVER_URL


def get_skany_video_info(time: time, camera_ip: str) -> Dict[str, Any]:
    request_data: Dict[str, Any] = {
        "camera_ip": camera_ip,
        "time": time,
    }

    try:
        response: requests = requests.post(
            url=f"{SERVER_URL}:3456/is_video_available/",
            json=request_data,
        )
    except Exception:
        return {"status": False}

    result: Dict[str, Any] = response.json()
    result["camera_ip"]: str = camera_ip

    return result
