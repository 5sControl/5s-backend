import requests
import logging

from typing import Any, Dict, Iterable, List

from src.Core.const import SERVER_URL

from src.Core.exceptions import InvalidResponseError, SenderError
from src.Core.utils import Sender
from src.Inventory.models import Items
from src.OrderView.models import IndexOperations
from src.Cameras.models import Camera
from src.Algorithms.models import Algorithm, CameraAlgorithm

from .logs_services import logs_service

logger = logging.getLogger(__name__)


def CreateCameraAlgorithms(camera_algorithm_data: Dict[str, Any]) -> None:
    camera: Dict[str, str] = camera_algorithm_data["camera"]
    algorithms: List[Dict[str, Any]] = camera_algorithm_data["algorithms"]

    create_camera(camera)
    logger.warning("Camera created successfully")
    create_camera_algorithms(camera, algorithms)


def CheckConnection(camera_data: Dict[str, str]) -> bool:
    try:
        response = Sender("add_camera", camera_data)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/add_camera") from e

    return response["status"]


def DeleteCamera(camera_instance):
    query_list_cameraalgorithms: Iterable[
        CameraAlgorithm
    ] = CameraAlgorithm.objects.filter(camera=camera_instance)

    for camera_algorithm in query_list_cameraalgorithms:
        pid: int = camera_algorithm.process_id
        if camera_algorithm.algorithm.name == "operation_control":
            IndexOperations.objects.get(camera=camera_algorithm.camera).delete()
        stop_camera_algorithm(pid)
        update_status_algorithm(pid)

    camera_id: int = camera_instance.id
    camera_instance.delete()

    return {
        "status": True,
        "message": f"Camera {camera_id} was successfully deleted.",
    }


def create_camera(camera: Dict[str, str]) -> None:
    ip: str = camera["ip"]
    name: str = camera["name"]
    username: str = camera["username"]
    password: str = camera["password"]

    camera_request: Dict[str, str] = {
        "ip": ip,
        "username": username,
        "password": password,
    }

    camera_data: Dict[str, str] = {
        "id": ip,
        "name": name,
        "username": username,
        "password": password,
    }

    is_camera_exist: Iterable[Camera] = Camera.objects.filter(
        id=ip, name=name, username=username, password=password
    ).exists()
    if is_camera_exist:
        return

    try:
        camera_obj_to_update = Camera.objects.get(id=ip)
    except Camera.DoesNotExist:
        Camera.objects.create(**camera_data, is_active=True)
        return
    else:
        camera_obj_to_update.name: str = name
        camera_obj_to_update.username: str = username
        camera_obj_to_update.password: str = password
        camera_obj_to_update.save()
        return


def create_camera_algorithms(
    camera: Dict[str, str], algorithms: List[Dict[str, Any]]
) -> None:
    camera_obj = Camera.objects.get(id=camera["ip"])
    new_records = [algorithm_data["name"] for algorithm_data in algorithms]
    existing_algorithms = [
        ca.algorithm.name for ca in CameraAlgorithm.objects.filter(camera=camera_obj)
    ]

    algorithm_to_delete = set(existing_algorithms) - set(new_records)
    new_algorithms = set(new_records) - set(existing_algorithms)

    algorithms = [
        algorithm_data
        for algorithm_data in algorithms
        if algorithm_data["name"] in new_algorithms
    ]

    for algorithm in algorithms:
        algorithm_obj = Algorithm.objects.get(name=algorithm["name"])
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
                type_operation=algorithm["config"]["operation_control_id"],
                camera=camera_obj,
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
            algorithm=algorithm_obj,
            camera=camera_obj,
            process_id=response["pid"],
        )
        new_record.save()

        logger.warning(f"New record -> {algorithm_obj.name} on camera {camera_obj.id}")

    for algorithm_name in algorithm_to_delete:
        algorithm: Algorithm = CameraAlgorithm.objects.get(
            algorithm__name=algorithm_name, camera=camera_obj
        )
        pid: int = algorithm.process_id

        if algorithm_name == "operation_control":
            IndexOperations.objects.get(camera=camera_obj).delete()

        stop_camera_algorithm(pid)
        update_status_algorithm(pid)

        logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")


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


def stop_camera_algorithm(pid: int) -> Dict[str, Any]:
    cstm_port = None
    algorithm_name = CameraAlgorithm.objects.get(process_id=pid).algorithm.name
    camera_id = CameraAlgorithm.objects.get(process_id=pid).camera.id
    if algorithm_name == "min_max_control":
        cstm_port = 3020

    try:
        response = Sender("stop", {"pid": pid}, cstm_port=cstm_port)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/stop") from e
    
    logger.warning(f"[INFO] Stopping camera algorithm. Algorithm: {algorithm_name}, camera: {camera_id}, PID: {pid}")
    logger.warning(response)
    if not response["status"]:
        raise InvalidResponseError("/stop", response["status"])

    return response


def update_status_algorithm(pid: int):
    camera_algorithm = CameraAlgorithm.objects.filter(process_id=pid).first()
    if camera_algorithm:
        logs_service.delete_log(
            algorithm_name=camera_algorithm.algorithm.name,
            camera_ip=camera_algorithm.camera.id,
        )
        camera_algorithm.delete()
