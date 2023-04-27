import requests

from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from src.CompanyLicense.decorators import check_active_cameras
from src.Algorithms.models import CameraAlgorithm
from src.Algorithms.services.edit_algorithms import edit_algorithms
from src.Algorithms.utils import yolo_proccesing

from src.Core.const import SERVER_URL

from src.Cameras.models import Camera
from src.Cameras.serializers import CameraSerializer


class CameraService:
    @check_active_cameras
    def create_camera(self, camera_info):
        ip = camera_info["ip"]
        username = camera_info["username"]
        password = camera_info["password"]

        result = self.check_ip(ip, username, password)

        if not result:
            return {
                "status": False,
                "snapshot": None,
                "ip": ip,
                "message": f"Connection to camera {ip} failed. Cannot get camera's snapshot.",
            }

        camera_data = {
            "id": ip,
            "username": username,
            "password": password,
        }
        serializer = CameraSerializer(data=camera_data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except ValidationError as e:
            return {"status": False, "error": f"ValidationError: {str(e)}"}
        except Exception as e:
            return {"status": False, "error": f"Exception: {str(e)}"}

        return {
            "status": True,
            "snapshot": result["result"],
            "ip": ip,
            "message": f"Camera with id {ip} was successfully saved.",
        }

    def check_ip(self, ip, username, password):
        camera_request_data = {
            "username": username,
            "password": password,
            "ip": ip
        }
        try:
            connect = requests.post(
                f"{SERVER_URL}:3456/add_camera", json=camera_request_data
            )
        except Exception:
            return False
        else:
            return connect.json()

    def update_camera_info(self, camera_data):
        camera_id = camera_data["ip"]
        camera_name = camera_data.get("username")

        try:
            camera = Camera.objects.get(id=camera_id)
        except ObjectDoesNotExist:
            return {
                "status": False,
                "message": f"Camera with id {camera_id} does not exist",
            }

        if camera_name is not None:
            camera.username = camera_name

        try:
            camera.full_clean()
            camera.save()
        except ValidationError as e:
            return {
                "status": False,
                "message": f"Failed to update camera with the id {camera_id}: {str(e)}",
            }
        else:
            return {
                "status": True,
                "message": f"Camera with the id {camera_id} has been successfully updated",
            }

    def delete_camera(self, camera_instance):
        query_list_cameraalgorithms = CameraAlgorithm.objects.filter(camera=camera_instance)

        for camera_algorithm in query_list_cameraalgorithms:
            pid = camera_algorithm.process_id
            result_stop_process = yolo_proccesing.stop_process(pid)
            if not result_stop_process["success"]:
                return {
                    "status": False,
                    "message": f"Can't stop process on camera {camera_algorithm.camera} algorithm {camera_algorithm.algorithm}.",
                }
            edit_algorithms.update_status_of_algorithm_by_pid(pid)

        try:
            camera_id = camera_instance.id
            camera_instance.delete()
        except Exception as e:
            return {
                "status": False,
                "message": f"Failed to delete camera {camera_id}: {str(e)}.",
            }

        return {
            "status": True,
            "message": f"Camera {camera_id} was successfully deleted.",
        }

    def is_camera_exist(self, camera_id):
        try:
            Camera.objects.get(id=camera_id)
        except ObjectDoesNotExist:
            return False
        else:
            return True


camera_service = CameraService()
