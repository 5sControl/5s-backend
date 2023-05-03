from src.Algorithms.models import CameraAlgorithm
from src.Algorithms.service import algorithms_services
from src.Algorithms.utils import yolo_proccesing

from src.Cameras.models import Camera


def delete_camera(camera_id):
    query_list_cameraalgorithms = CameraAlgorithm.objects.filter(camera=camera_id)

    for camera_algorithms in query_list_cameraalgorithms:
        pid = camera_algorithms.process_id
        result_stop_process = yolo_proccesing.stop_process(pid)
        if not result_stop_process["status"]:
            return {
                "status": False,
                "message": f"Can't stop process on camera {camera_algorithms.camera} algorithm {camera_algorithms.algorithm}"
            }
        algorithms_services.update_status_of_algorithm_by_pid(pid)

    camera = Camera.objects.filter(id=camera_id)
    if not camera:
        return {
            "status": False,
            "message": f"Camera {camera_id} does not exist"
        }
    else:
        camera.delete()
        return {
            "status": True,
            "message": f"Camera {camera_id} was successfully deleted."
        }
