import requests

from src.Algorithms.models import Algorithm
from src.Cameras.models import Camera

from src.Cameras.service import link_generator


class StartYoloProccesing:
    def start_yolo_processing(self, camera: Camera, algorithm: Algorithm, url: str):
        rtsp_camera_url = link_generator.get_camera_rtsp_link_by_camera(camera)
        response = {
            "camera_url": rtsp_camera_url["camera_url"],
            "algorithm": algorithm.name,
            "server_url": url,
        }
        try:
            response = requests.post(
                url=f"{url}:3020/run",
                json=response,
            )
            response_json = response.json()
            response_json["server_url"] = url
            print(response_json)
            if not response_json["success"]:
                return {
                    "status": False,
                    "message": f"Received non-success response: {response_json}",
                }
            elif "pid" not in response_json:
                return {
                    "status": False,
                    "message": f"Missing PID in response: {response_json}",
                }
            response_json["status"] = True
            return response_json
        except requests.exceptions.RequestException as e:
            return {
                "status": False,
                "message": [f"Error sending/decoding request: {e}"],
            }
        except (AttributeError, ValueError):
            return {
                "status": False,
                "message": "The process was not set in motion. No response from Yolo",
            }


yolo_proccesing = StartYoloProccesing()
