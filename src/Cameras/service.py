from django.core.exceptions import ValidationError
import requests

from .models import Camera

from src.core.logger import logger


class CameraLinkGenerator:
    def get_camera_http_link(self):
        """
        Create http for each camera

        example -> http://admin-onvif:admin@192.168.1.160/onvif-http/snapshot?Profile_1
        """
        cameras_info = Camera.objects.all()
        result = []
        for camera_info in cameras_info:
            camera_data = {
                "ip": camera_info.id,
                "camera_url": f"http://{camera_info.username}:{camera_info.password}@{camera_info.id}/onvif-http/snapshot?Profile_1",
            }
            result.append(camera_data)

        return result

    def get_camera_rtsp_link(self, ip, username, password):
        """
        Create rtsp using the given camera data

        example -> rtsp://admin:admin@192.168.1.160/h264_stream
        """
        camera_rtsp_link = f"rtsp://{username}:{password}@{ip}/h264_stream"
        return camera_rtsp_link

    def get_camera_http_link_by_camera(self, camera_id):
        """
        Create a http link for a given camera
        """
        cameras_data = Camera.objects.filter(id=camera_id.id).first()
        if cameras_data:
            camera_rtsp_link = f"http://{cameras_data.username}:{cameras_data.password}@{cameras_data.id}/onvif-http/snapshot?Profile_1"
            return {"status": True, "camera_url": camera_rtsp_link}
        else:
            return {"status": False, "camera_url": None}

    def get_camera_rtsp_link_by_camera(self, camera_id):
        """
        Create a rtsp link for a given camera
        """
        cameras_data = Camera.objects.filter(id=camera_id.id).first()
        if cameras_data:
            camera_rtsp_link = f"rtsp://{cameras_data.username}:{cameras_data.password}@{cameras_data.id}/h264_stream"
            return {"status": True, "camera_url": camera_rtsp_link}
        else:
            return {"status": False, "camera_url": None}


class CameraService:
    """
    Save the camera with extra information and run yolo processing
    """

    def create_camera(self, camera_info):
        """
        This method will create a camera,
        if it is possible to get a snapshot with the received data,
        otherwise an error will be returned
        """

        ip = camera_info["ip"]
        username = camera_info["username"]
        password = camera_info["password"]
        camera_url = camera_info["url"]

        if ip:  # check if ip was sended
            logger.info(f"IP {ip}")
            snapshot_request = self.check_ip(ip, username, password, camera_url)
            snapshot = snapshot_request.json()
        else:
            return {"status": False, "message": f"Ip not defined"}
        if snapshot["status"]:  # check if snapshot was recived successfully
            camera = Camera(
                id=ip,
                username=username,
                password=password,
            )
        else:
            return {
                "status": False,
                "snapshot": None,
                "ip": ip,
                "message": f"connection to camera {ip} failed. cannot get cameras snapshot",
            }
        try:
            camera.full_clean()
            camera.save()
        except ValidationError as e:
            return {"status": "failure", "error": f"ValidationError: {str(e)}"}
        except KeyError as e:
            return {"status": "failure", "error": f"KeyError: {str(e)}"}
        except Exception as e:
            return {"status": "failure", "error": f"Exception: {str(e)}"}
        else:
            return {
                "status": True,
                "snapshot": snapshot["result"],
                "ip": ip,
                "message": f"Camera with id {ip} was successfully saved",
            }

    def check_ip(self, ip, username, password, url):
        """
        get camera information, generate link and send it to
        fastapi application to get snapshot and convert to base64

        if succes -> return {"status": True, "result": snapshot}
        if fail -> return {"status": False, "message": ip}
        """
        rtsp_link = f"rtsp://{username}:{password}@{ip}/h264_stream"
        camera_request_data = {"camera_url": rtsp_link, "ip": ip}
        try:
            connect = requests.post(
                connect=requests.post(
                    f"{url}find_camera_image", json=camera_request_data  # fastapi link
                ),
            )
            print(f"fastapi connection {connect.text}")
        except:
            return {
                "status": False,
                "message": f"Camera url not found -> {camera_request_data['camera_url']}",
            }
        else:
            return connect

    def get_cameras_by_ids(self, ids: str):
        return Camera.objects.filter(id__in=ids)

    def update_camera_info(self, camera_data: dict):
        camera_id = camera_data["ip"]
        camera_name = camera_data["name"]
        camera = Camera.objects.filter(id=camera_id).first()
        if camera:
            camera.name = camera_name
            camera.save()
            return {
                "status": True,
                "message": f"сamera with the id {camera_id} is named {camera_name}",
            }
        else:
            return {
                "status": False,
                "message": f"camera with ip {camera_id} does not exist",
            }


link_generator = CameraLinkGenerator()
camera_service = CameraService()
