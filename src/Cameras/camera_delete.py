from src.Algorithms.service import AlgorithmsService
from src.Algorithms.utils import yolo_proccesing
from src.Cameras.models import Camera
from src.Algorithms.service import algorithms_services


def delete_camera(camera_id):
    query_list_cameraalgorithms = AlgorithmsService.camera_algorithm_by_camera_id(
        camera_id
    )
    if query_list_cameraalgorithms:
        for camera_algorithms in query_list_cameraalgorithms:
            pid = camera_algorithms.process_id
            result_stop_process = yolo_proccesing.stop_process(pid)
            if not result_stop_process["status"]:
                return result_stop_process
            result_update_status = algorithms_services.update_status_of_algorithm_by_pid(pid)
            if not result_update_status["status"]:
                return result_update_status
    Camera.objects.filter(id=camera_id).delete()
    return {
        "status": True,
        "message": f"Camera {camera_id} was successfully deleted."
    }