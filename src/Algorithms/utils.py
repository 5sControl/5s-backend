import requests

from src.StaffControl.Locations.service import link_generator


class StartYoloProccesing:
    def start_yolo_processing(self, camera, algorithm, url):
        rtsp_camera_url = link_generator.get_camera_rtsp_link_by_camera(camera)
        response = {
            "camera_url": rtsp_camera_url["camera_link"],
            "algorithm": algorithm.name,
            "server_url": url,
        }
        try:
            response = requests.post(
                url=f"{url}:3020/run",  # Send process data to YOLOv7 server
                json=response,
            )
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            self.errors.append(f"Error sending request: {e}")
            return {"errors": [f"Error sending request: {e}"]}
        except ValueError as e:
            self.errors.append(f"Error decoding response: {e}")
            return {"errors": [f"Error decoding response: {e}"]}
        try:
            if response_json.get("status").lower() != "success":
                self.errors.append(f"Received non-success response: {response_json}")
                return {"errors": [f"Received non-success response: {response_json}"]}
            elif "pid" not in response_json:
                self.errors.append(f"Missing PID in response: {response_json}")
                return {"errors": [f"Missing PID in response: {response_json}"]}
        except AttributeError:
            return {
                "errors": "The process was not set in motion. No response from Yolo"
            }

        else:
            return response_json


yolo_proccesing = StartYoloProccesing()
