import requests
import logging

from typing import Any, Dict, Iterable, List, Optional, Set

from src.Core.exceptions import InvalidResponseError, SenderError, CameraConnectionError
from src.Core.utils import Sender
from src.Core.const import SERVER_URL
from src.Inventory.models import Items
from src.OrderView.models import IndexOperations
from src.CompanyLicense.decorators import check_active_cameras, check_active_algorithms

from ..models import Camera, ZoneCameras
from ..models import Algorithm, CameraAlgorithm
from .logs_services import logs_service

logger = logging.getLogger(__name__)


@check_active_cameras
@check_active_algorithms
def CreateCameraAlgorithms(camera_algorithm_data: Dict[str, Any]) -> None:
    camera: Dict[str, str] = camera_algorithm_data["camera"]
    algorithms: List[Dict[str, Any]] = camera_algorithm_data["algorithms"]

    create_camera(camera)
    logger.warning(f"Camera [{camera['ip']}] created successfully")
    create_camera_algorithms(camera, algorithms)


def check_connection(camera_data: Dict[str, str]) -> bool:
    try:
        response = Sender("add_camera", camera_data)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/add_camera") from e

    return response["status"]


def DeleteCamera(camera_instance: Camera) -> Dict[str, Any]:
    query_list_cameraalgorithms: Iterable[
        CameraAlgorithm
    ] = CameraAlgorithm.objects.filter(camera=camera_instance)

    for camera_algorithm in query_list_cameraalgorithms:
        pid: int = camera_algorithm.process_id
        stop_and_update_algorithm(pid)

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

    if not check_connection({"ip": ip, "username": username, "password": password}):
        raise CameraConnectionError(ip)

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
    camera_obj: Camera = Camera.objects.get(id=camera["ip"])

    algo_ids_to_delete: List[int] = get_algorithm_ids_to_delete(camera_obj, algorithms)
    
    for camera_algo_id in algo_ids_to_delete:
        pid: int = CameraAlgorithm.objects.get(id=camera_algo_id).process_id
        stop_and_update_algorithm(pid)
        logger.warning(f"Successfully deleted pid {pid}")

    for algorithm in algorithms:
        algorithm_obj: Algorithm = Algorithm.objects.get(name=algorithm["name"])
        algorithm_name: str = algorithm["name"]

        rtsp_link: str = camera_rtsp_link(camera_obj.id)

        zones: List[Optional[Dict[str, Any]]] = []
        data: List[Dict[str, Any]] = []
        response: Dict = {}
        areas: List[Dict[str, Any]] = []
        stelag: List[Dict[str, Any]] = []

        request: Dict[str, Any] = {
            "camera_url": rtsp_link,
            "algorithm": algorithm_obj.name,
            "server_url": SERVER_URL,
            "extra": data,
        }
        
        zones: List[Optional[Dict[str, int]]] = algorithm.get("config", {}).get("zonesID", [])

        if algorithm_name == "min_max_control":
            if compare_zones(algorithm_obj, camera_obj, zones):
                pid: int = CameraAlgorithm.objects.get(algorithm=algorithm_obj, camera=camera_obj).process_id
                stop_and_update_algorithm(pid)
                logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")

                continue

            algorithm_items: Items = Items.objects.filter(camera=camera_obj.id)
            for item in algorithm_items:
                areas.append(
                    {"itemId": item.id, "itemName": item.name, "coords": item.coords}
                )

            for zone_id in zones:
                zone_camera = ZoneCameras.objects.get(
                    id=zone_id["id"], camera=camera_obj
                )

                stelag.append(
                    {
                        "zoneId": zone_camera.id,
                        "zoneName": zone_camera.name,
                        "coords": zone_camera.coords,
                    }
                )

            new_data: Dict[str, List[Dict[str, int]]] = {"areas": areas, "zones": stelag}

            data.append(new_data)

            request["extra"] = data
            response: Dict[str, Any] = send_run_request(request)

        if algorithm_name == "machine_control":
            if compare_zones(algorithm_obj, camera_obj, zones):
                pid: int = CameraAlgorithm.objects.get(algorithm=algorithm_obj, camera=camera_obj).process_id
                stop_and_update_algorithm(pid)
                logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")

                continue

            for zone_id in zones:
                zone_camera = ZoneCameras.objects.get(
                    id=zone_id["id"], camera=camera_obj
                )
                coords = zone_camera.coords
                coords[0]["zoneId"] = zone_camera.id
                coords[0]["zoneName"] = "zone " + str(zone_camera.name)

                new_object = [{"coords": coords}]

                data.append(new_object)

            request["extra"] = data

            response: Dict[str, Any] = send_run_request(request)

        if algorithm_name == "idle_control":
            if CameraAlgorithm.objects.filter(algorithm=algorithm_obj, camera=camera_obj).exists():
                stop_and_update_algorithm(pid)
                logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")

            response: Dict[str, Any] = send_run_request(request)

        if algorithm_name == "operation_control":
            operation_control_id: int = algorithm["config"]["operation_control_id"]
            index_operations_obj: IndexOperations = IndexOperations.objects.filter(type_operation=operation_control_id, camera=camera_obj)

            if index_operations_obj.exists():
                continue
            else:
                index_operations_obj.delete()
                stop_and_update_algorithm(pid)
                logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")
            
            index_operation: IndexOperations = IndexOperations(
                type_operation=operation_control_id,
                camera=camera_obj,
            )
            index_operation.save()

            response: Dict[str, Any] = send_run_request(request)

        if algorithm_name == "safety_control_ear_protection":
            if CameraAlgorithm.objects.filter(algorithm=algorithm_obj, camera=camera_obj).exists():
                stop_and_update_algorithm(pid)
                logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")
    
            response: Dict[str, Any] = send_run_request(request)

        if algorithm_name == "safety_control_head_protection":
            if CameraAlgorithm.objects.filter(algorithm=algorithm_obj, camera=camera_obj).exists():
                stop_and_update_algorithm(pid)
                logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")
    
            response: Dict[str, Any] = send_run_request(request)

        if algorithm_name == "safety_control_hand_protection":
            if CameraAlgorithm.objects.filter(algorithm=algorithm_obj, camera=camera_obj).exists():
                stop_and_update_algorithm(pid)
                logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")
    
            response: Dict[str, Any] = send_run_request(request)

        if algorithm_name == "safety_control_reflective_jacket":
            if CameraAlgorithm.objects.filter(algorithm=algorithm_obj, camera=camera_obj).exists():
                stop_and_update_algorithm(pid)
                logger.warning(f"Successfully deleted -> {algorithm_name} with pid {pid}")
    
            response: Dict[str, Any] = send_run_request(request)

        new_record: CameraAlgorithm = CameraAlgorithm(
            algorithm=algorithm_obj,
            camera=camera_obj,
            process_id=response["pid"],
            zones=zones,
        )
        new_record.save()

        if zones is not None:
            update_status_zones_true(zones)

        logger.warning(f"New record -> {algorithm_obj.name} on camera {camera_obj.id}")
        return


def camera_rtsp_link(id: str) -> str:
    cameras_data = Camera.objects.get(id=id)
    return f"rtsp://{cameras_data.username}:{cameras_data.password}@{cameras_data.id}/h264_stream"


def get_algorithm_ids_to_delete(camera_obj: Camera, algorithms: List[Dict[str, Any]]) -> List[int]:
    algorithm_names: List[str] = [algo["name"] for algo in algorithms]
    existing_algorithms: Iterable[CameraAlgorithm] = CameraAlgorithm.objects.filter(camera=camera_obj, algorithm__name__in=algorithm_names)
    existing_algorithm_ids: Set[int] = set(algorithm.id for algorithm in existing_algorithms)
    algorithms_to_delete: List[int] = [id for id in existing_algorithm_ids if id not in algorithm_names]
    return algorithms_to_delete


def send_run_request(request: Dict[str, Any]) -> Dict[str, Any]:
    logger.warning(f"Request data for algorithm {request}")
    try:
        response = Sender("run", request)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/run") from e
    if not response["status"]:
        raise InvalidResponseError("/run", response["status"])

    return response


def stop_and_update_algorithm(pid: int) -> None:
    algo_name: str = CameraAlgorithm.objects.get(process_id=pid).algorithm.name
    camera_ip: str = CameraAlgorithm.objects.get(process_id=pid).camera.id

    if algo_name == "operation_control":
            IndexOperations.objects.filter(camera=camera_ip).delete()

    stop_camera_algorithm(pid)
    update_status_algorithm(pid)


def stop_camera_algorithm(pid: int) -> Dict[str, Any]:
    cstm_port = None
    algorithm_name = CameraAlgorithm.objects.get(process_id=pid).algorithm.name
    camera_id = CameraAlgorithm.objects.get(process_id=pid).camera.id

    try:
        response = Sender("stop", {"pid": pid}, cstm_port=cstm_port)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/stop") from e

    logger.warning(
        f"[INFO] Stopping camera algorithm. Algorithm: {algorithm_name}, camera: {camera_id}, PID: {pid}"
    )
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

        if camera_algorithm.zones is not None:
            update_status_zone_false(camera_algorithm.zones)

        camera_algorithm.delete()


def update_status_zone_false(data):
    """Update status zone in the end"""

    for zone in data:
        zone_id = zone.get("id")
        if zone_id:
            try:
                zone_obj = ZoneCameras.objects.get(id=zone_id)
                zone_obj.is_active = False
                zone_obj.save()
            except ZoneCameras.DoesNotExist:
                pass


def update_status_zones_true(zones):
    """Update status zones on True"""

    for zone in zones:
        zone_id = zone.get("id")
        if zone_id:
            try:
                zone_obj = ZoneCameras.objects.get(id=zone_id)
                zone_obj.is_active = True
                zone_obj.save()
            except ZoneCameras.DoesNotExist:
                pass


def compare_zones(algorithm_obj: Algorithm, camera_obj: Camera, zones: List[Dict[str, int]]) -> bool:
    if CameraAlgorithm.objects.filter(algorithm=algorithm_obj, camera=camera_obj).exists():
        camera_algorithm = CameraAlgorithm.objects.get(algorithm=algorithm_obj, camera=camera_obj)
        saved_zones = camera_algorithm.zones
        if saved_zones == zones:
            return True
    return False
