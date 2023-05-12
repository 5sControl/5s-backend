import requests


from src.Core.const import SERVER_URL


def get_skany_video_info(time, camera_ip):
    response = {
        "camera_ip": camera_ip,
        "time": time,
    }
    try:
        request = requests.post(
            url=f"{SERVER_URL}:3456/is_video_available/",
            json=response,
        )
    except Exception:
        return {"status": False}

    result = request.json()
    result["camera_ip"] = camera_ip

    print(f"[RESULT VIDEO INFO] {result}")
    return result
