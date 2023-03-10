import requests

from src.Cameras.service import link_generator

from src.Algorithms.models import Algorithm, CameraAlgorithm
from src.Cameras.models import Camera


class YoloProccesing:
    def start_yolo_processing(
        self, camera: Camera, algorithm: Algorithm, url: str
    ) -> dict:
        rtsp_camera_url = link_generator.get_camera_rtsp_link_by_camera(camera)
        response = {
            "camera_url": rtsp_camera_url["camera_url"],
            "algorithm": algorithm.name,
            "server_url": url,
        }
        request = requests.post(
            url=f"{url}:3333/run",
            json=response,
        )
        request_json = request.json()
        request_json["server_url"] = url
        request_json["status"] = True

        return request_json

    def stop_process(self, pid: int):
        is_pid_exists = self.is_pid_exists(pid)
        if not is_pid_exists:
            return {"status": False, "message": "PID not found"}

        yolo_server_url = self.get_yolo_url(pid)

        request = requests.post(
            url=f"{yolo_server_url}:3333/stop",
            json={"pid": pid},
        )
        response_json = request.json()
        print(response_json)

        return response_json

    def is_pid_exists(self, pid: int):
        camera_algorithm = CameraAlgorithm.objects.filter(process_id=pid).first()
        if not camera_algorithm:
            return False
        else:
            return True

    def get_yolo_url(self, pid=None):
        if pid:
            url = CameraAlgorithm.objects.filter(process_id=pid).first()

        return url.yolo_url


yolo_proccesing = YoloProccesing()
