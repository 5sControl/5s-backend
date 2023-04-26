from src.Algorithms.models import CameraAlgorithm
from src.Algorithms.service import algorithms_services
from src.Algorithms.utils import yolo_proccesing

from src.Cameras.models import Camera


def delete_camera(camera_id):
    query_list_cameraalgorithms = CameraAlgorithm.objects.filter(camera=camera_id)

    if query_list_cameraalgorithms:
        for camera_algorithms in query_list_cameraalgorithms:
            pid = camera_algorithms.process_id
            result_stop_process = yolo_proccesing.stop_process(pid)
            if not result_stop_process["success"]:
                return result_stop_process
            result_update_status = algorithms_services.update_status_of_algorithm_by_pid(pid)
            if not result_update_status["status"]:
                return result_update_status
    else:
        return {
            "status": True,
            "message": f"Camera {camera_id} does not exist"
        }
    Camera.objects.filter(id=camera_id).delete()
    return {
        "status": True,
        "message": f"Camera {camera_id} was successfully deleted."
    }
