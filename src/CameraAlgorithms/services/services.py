import requests

from typing import Any, Dict, List

from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from src.Core.const import SERVER_URL

from src.Core.exceptions import InvalidResponseError, SenderError
from src.Core.utils import Sender
from src.Inventory.models import Items
from src.OrderView.models import IndexOperations

from ..serializers import CameraModelSerializer
from ..services.logs_services import logs_service
from ..models.algorithm import Algorithm, CameraAlgorithm
from ..models.camera import Camera


def CreateCameraAlgorithms(data: Dict[str, Any]) -> None:
    camera: Dict[str, str] = data["camera"]
    algorithms: List[Dict[str, Any]] = data["algorithms"]

    create_camera(camera)
    create_camera_algorithms(camera, algorithms)


def UpdateCameraInfo(camera_data):
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


def DeleteCamera(camera_instance):
    query_list_cameraalgorithms = CameraAlgorithm.objects.filter(camera=camera_instance)

    for camera_algorithm in query_list_cameraalgorithms:
        pid: int = camera_algorithm.process_id
        StopCameraAlgorithm(pid)
        UpdateStatusAlgorithm(pid)

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


def create_camera(camera: Dict[str, str]) -> None:
    ip: str = camera["ip"]
    name: str = camera["name"]
    username: str = camera["username"]
    password: str = camera["password"]

    camera_data: Dict[str, str] = {
        "ip": ip,
        "name": name,
        "username": username,
        "password": password,
    }

    try:
        Sender("add_camera", camera_data)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/add_camera") from e

    serializer = CameraModelSerializer(data=camera_data)
    serializer.is_valid(raise_exception=True)

    serializer.save()


def create_camera_algorithms(
    camera: Dict[str, str], algorithms: List[Dict[str, Any]]
) -> None:
    camera_obj = Camera.objects.get(id=camera["ip"])

    for algorithm in algorithms:
        algorithm_obj = Algorithm.objects.get(id=algorithm["name"])
        rtsp_link: str = camera_rtsp_link(camera_obj.id)
        data: List[Dict[str, Any]] = []
        response: Dict = {}

        request: Dict[str, Any] = {
            "camera_url": rtsp_link,
            "algorithm": algorithm_obj.name,
            "server_url": SERVER_URL,
            "extra": data,
        }

        if algorithm_obj.name == "min_max_control":
            algorithm_items = Items.objects.filter(camera=camera_obj.id)
            for item in algorithm_items:
                data.append(
                    {"itemId": item.id, "coords": item.coords, "itemName": item.name}
                )

            request["extra"] = data

            response = send_run_request(request)

        if algorithm_obj.name == "idle_control":
            response = send_run_request(request)

        if algorithm_obj.name == "machine_control":
            response = send_run_request(request)

        if algorithm_obj.name == "operation_control":
            indx_operation = IndexOperations(
                type_operation=algorithm["config"]["operation_control_id"]
            )
            indx_operation.save()
            response = send_run_request(request)

        if algorithm_obj.name == "safety_control_ear_protection":
            response = send_run_request(request)

        if algorithm_obj.name == "safety_control_head_protection":
            response = send_run_request(request)

        if algorithm_obj.name == "safety_control_hand_protection":
            response = send_run_request(request)

        if algorithm_obj.name == "safety_control_reflective_jacket":
            response = send_run_request(request)

        new_record = CameraAlgorithm(
            algorithm=algorithm,
            camera=camera,
            process_id=response["pid"],
        )
        new_record.save()


def camera_rtsp_link(id: str) -> str:
    cameras_data = Camera.objects.get(id=id)
    return f"rtsp://{cameras_data.username}:{cameras_data.password}@{cameras_data.id}/h264_stream"


def send_run_request(request: Dict[str, Any]) -> Dict[str, Any]:
    try:
        response = Sender("run", request)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/run") from e
    if not response["status"]:
        raise InvalidResponseError("/run", response["status"])

    return response


def StopCameraAlgorithm(pid: int) -> Dict[str, Any]:
    cstm_port = None
    algorithm_name = CameraAlgorithm.objects.get(process_id=pid).algorithm.name
    if algorithm_name == "min_max_control":
        cstm_port = 3020
    try:
        response = Sender("stop", {"pid": pid}, cstm_port=cstm_port)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/stop") from e
    if not response["status"]:
        raise InvalidResponseError("/stop", response["status"])

    return response


def UpdateStatusAlgorithm(pid: int):
    camera_algorithm = CameraAlgorithm.objects.filter(process_id=pid).first()
    if camera_algorithm:
        logs_service.delete_log(
            algorithm_name=camera_algorithm.algorithm.name,
            camera_ip=camera_algorithm.camera.id,
        )
        camera_algorithm.delete()
