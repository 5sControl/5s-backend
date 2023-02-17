from django.core.exceptions import ValidationError
import requests

from .models import Camera


class CameraLinkGenerator:
    """"""

    def create_camera(self, camera_info):
        """Save the camera with extra information"""
        if camera_info["ip"]:
            rtsp_link = self.get_camera_rtsp_link(
                ip=camera_info["ip"],
                username=camera_info["username"],
                password=camera_info["password"],
            )
            camera_data = {"link": rtsp_link, "ip": camera_info["ip"]}
            request = requests.post(
                f"{camera_info['url']}find_camera_image",
                params=camera_data,
            )
            print(request.text)
            if request.json()["status"]:
                camera = Camera(
                    id=camera_info["ip"],
                    username=camera_info["username"],
                    password=camera_info["password"],
                )
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
                    "message": f'Camera with id {camera_info["ip"]} was successfully saved'
                }
        else:
            return {"message": "ip was not found"}

    def get_camera_http_link(self):
        """
        Create link for each camera

        example -> http://admin-onvif:admin@192.168.1.160/onvif-http/snapshot?Profile_1
        """
        cameras_info = Camera.objects.all()
        result = []
        for camera_info in cameras_info:
            camera_data = {
                "ip": camera_info.id,
                "link": f"http://{camera_info.username}:{camera_info.password}@{camera_info.id}/onvif-http/snapshot?Profile_1",
            }
            result.append(camera_data)

        return result

    def get_camera_rtsp_link(self):
        """
        Create link for each camera

        example -> rtsp://admin:just4Taqtile@192.168.1.161/h264_stream
        """
        cameras_info = Camera.objects.all()
        result = []
        for camera_info in cameras_info:
            camera_data = {
                "ip": camera_info.id,
                "link": f"rtsp://{camera_info.username}:{camera_info.password}@{camera_info.id}/h264_stream",
            }
            result.append(camera_data)

        return result

    def get_camera_rtsp_link(self, ip, username, password):
        """
        Create link using the given camera data
        """
        camera_rtsp_link = f"rtsp://{username}:{password}@{ip}/h264_stream"
        return camera_rtsp_link

    def get_camera_rtsp_link_by_camera(self, camera_data):
        """
        Create a rtsp link for a given camera
        """
        cameras_info = Camera.objects.filter(id=camera_data["ip"]).first()
        if cameras_info:
            camera_rtsp_link = f"rtsp://{cameras_info.username}:{cameras_info.password}@{cameras_info.id}/h264_stream"
            return {"status": True, "camera_link": camera_rtsp_link}
        else:
            return {"status": False, "camera_link": None}


link_generator = CameraLinkGenerator()
