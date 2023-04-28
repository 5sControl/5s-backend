import requests

from src.Core.const import SERVER_URL


def send_request_to_update_service(service):
    print(f"Sending request to update service {service}")
    request = requests.post(f"{SERVER_URL}/deploy?service={service}")
    return request.status_code
