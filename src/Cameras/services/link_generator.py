from src.Cameras.models import Camera


class CameraLinkGenerator:
    def get_camera_http_link(self):
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
        camera_rtsp_link = f"rtsp://{username}:{password}@{ip}/h264_stream"
        return camera_rtsp_link

    def get_camera_http_link_by_camera(self, camera_id):
        cameras_data = Camera.objects.filter(id=camera_id.id).first()
        if cameras_data:
            camera_rtsp_link = f"http://{cameras_data.username}:{cameras_data.password}@{cameras_data.id}/onvif-http/snapshot?Profile_1"
            return {"status": True, "camera_url": camera_rtsp_link}
        else:
            return {"status": False, "camera_url": None}

    def get_camera_rtsp_link_by_camera(self, camera_id):
        cameras_data = Camera.objects.filter(id=camera_id.id).first()
        if cameras_data:
            camera_rtsp_link = f"rtsp://{cameras_data.username}:{cameras_data.password}@{cameras_data.id}/h264_stream"
            return {"status": True, "camera_url": camera_rtsp_link}
        else:
            return {"status": False, "camera_url": None}


link_generator = CameraLinkGenerator()
