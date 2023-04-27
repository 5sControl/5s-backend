import requests

from src.Cameras.services.link_generator import link_generator

from src.Algorithms.models import CameraAlgorithm

from src.Core.const import SERVER_URL


class YoloProccesing:
    def start_yolo_processing(
        self, camera, algorithm, data=None
    ):
        port = 3333
        rtsp_camera_url = link_generator.get_camera_rtsp_link_by_camera(camera)
        response = {
            "camera_url": rtsp_camera_url["camera_url"],
            "algorithm": algorithm.name,
            "server_url": SERVER_URL,
            "extra": data,
        }

        request = requests.post(
            url=f"{SERVER_URL}:{port}/run",
            json=response,
        )

        request_json = request.json()
        request_json["server_url"] = SERVER_URL
        request_json["status"] = True

        return request_json

    def stop_process(self, pid: int):
        is_pid_exists = self.is_pid_exists(pid)
        port = 3333
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
