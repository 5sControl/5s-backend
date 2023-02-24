import requests

from src.Algorithms.models import Algorithm
from src.Cameras.models import Camera

from src.Cameras.service import link_generator


class StartYoloProccesing:
	def start_yolo_processing(self, camera: Camera, algorithm: Algorithm, url: str) -> dict:
		rtsp_camera_url = link_generator.get_camera_rtsp_link_by_camera(camera)
		response = {
			"camera_url": rtsp_camera_url["camera_url"],
			"algorithm": algorithm.name,
			"server_url": url,
		}
		response = requests.post(
			url=f"{url}:3020/run",
			json=response,
		)
		response_json = response.json()
		response_json["server_url"] = url
		response_json["status"] = True
		
		return response_json



yolo_proccesing = StartYoloProccesing()
