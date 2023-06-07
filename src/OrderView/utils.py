import requests


from src.Core.const import SERVER_URL


def get_skany_video_info(time, camera_ip):
    request_data = {
        "camera_ip": camera_ip,
        "time": time,
    }
    try:
        response = requests.post(
            url=f"{SERVER_URL}:3456/is_video_available/",
            json=request_data,
        )
    except Exception:
        return {"status": False}

    result = response.json()
    result["camera_ip"] = camera_ip

    return result
