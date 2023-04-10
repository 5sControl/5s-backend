import os
import requests

from src.Cameras.service import link_generator

from src.Algorithms.models import Algorithm, CameraAlgorithm
from src.Cameras.models import Camera
min_max_ids = []

class YoloProccesing:
    def start_yolo_processing(
        self, camera: Camera, algorithm: Algorithm, url: str, data=None
    ) -> dict:
        rtsp_camera_url = link_generator.get_camera_rtsp_link_by_camera(camera)
        response = {
            "camera_url": rtsp_camera_url["camera_url"],
            "algorithm": algorithm.name,
            "server_url": url,
            "extra": data,
        }
        print("RESPONSE FOR ALGORITHM: ", response)
        port = 3333
        if algorithm.name == 'min_max_control':
            port = 3020
        request = requests.post(
            url=f"{url}:{port}/run",
            json=response,
        )
        print(f"ALGORITHM {algorithm.name}")
        request_json = request.json()
        request_json["server_url"] = url
        request_json["status"] = True
        if algorithm.name == 'min_max_control':
            min_max_ids.append(request_json["pid"])

        return request_json

    def stop_process(self, pid: int):
        is_pid_exists = self.is_pid_exists(pid)
        if not is_pid_exists:
            return {"status": False, "message": "PID not found"}

        yolo_server_url = self.get_algorithm_url()

        port = 3333
        if pid in min_max_ids:
            port = 3020
        while pid in min_max_ids:
            min_max_ids.remove(pid)

        request = requests.post(
            url=f"{yolo_server_url}:{port}/stop",
            json={"pid": pid},
        )
        response_json = request.json()

        return response_json

    def is_pid_exists(self, pid: int):
        camera_algorithm = CameraAlgorithm.objects.filter(process_id=pid).first()
        if not camera_algorithm:
            return False
        else:
            return True

    def get_algorithm_url(self):
        ALGORITHM_URL = os.environ.get("ALGORITHM_URL")

        return ALGORITHM_URL


yolo_proccesing = YoloProccesing()
