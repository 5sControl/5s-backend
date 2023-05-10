import os
import requests

from src.Cameras.service import link_generator

from src.Algorithms.models import CameraAlgorithm
from src.Core.const import SERVER_URL
MIN_MAX_PYTHON = os.environ.get("MIN_MAX_PYTHON")
IDLE_PYTHON = os.environ.get("IDLE_PYTHON")
python_algorithms = []

class YoloProccesing:
    def start_yolo_processing(
        self, camera, algorithm, data=None
    ) -> dict:
        rtsp_camera_url = link_generator.get_camera_rtsp_link_by_camera(camera)
        response = {
            "camera_url": rtsp_camera_url["camera_url"],
            "algorithm": algorithm.name,
            "server_url": SERVER_URL,
            "extra": data,
        }
        print("RESPONSE FOR ALGORITHM: ", response)

        port = 3333
        isPythonAlgorithm = False
        if algorithm.name == 'min_max_control' and MIN_MAX_PYTHON:
            port = 3020
            isPythonAlgorithm = True
        if algorithm.name == 'idle_control' and IDLE_PYTHON:
            port = 3020
            isPythonAlgorithm = True
        request = requests.post(
            url=f"{SERVER_URL}:{port}/run",
            json=response,
        )
        print(f"ALGORITHM {algorithm.name}")
        request_json = request.json()
        request_json["server_url"] = SERVER_URL
        try:
            if isPythonAlgorithm:
                python_algorithms.append(request_json["pid"])
        except:
            print('pid not exist')

        return request_json

    def stop_process(self, pid: int):
        is_pid_exists = self.is_pid_exists(pid)
        port = 3333
        if pid in python_algorithms:
            port = 3020
        while pid in python_algorithms:
            python_algorithms.remove(pid)
        url = f"{SERVER_URL}:{port}/stop"

        if not is_pid_exists:
            return {"status": False, "message": "PID not found"}

        request = requests.post(
            url=url,
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


yolo_proccesing = YoloProccesing()
