import requests

from src.Algorithms.utils import yolo_proccesing


HOST = yolo_proccesing.get_algorithm_url()


def send_request_to_update_service(service):
    print(f"Sending request to update service {service}")
    request = requests.post(f"{HOST}/deploy?service={service}")
    return request.status_code
