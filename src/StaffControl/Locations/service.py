from django.core.exceptions import ValidationError

from .models import Camera


def save_camera(data):
    """Save the camera with extra information"""

    for camera_info in data["cameras_info"]:
        if camera_info["ip"]:
            ...
        camera = Camera(
            id=camera_info["ip"],
            name=camera_info["name"],
            description=camera_info["description"],
            username=camera_info["username"],
            password=camera_info["password"],
        )
        try:
            camera.full_clean()
            camera.save()
        except ValidationError as e:
            return {"status": "failure", "error": f"ValidationError: {str(e)}"}
        except KeyError as e:
            return {"status": "failure", "error": f"KeyError: {str(e)}"}
        except Exception as e:
            return {"status": "failure", "error": f"Exception: {str(e)}"}
        else:
            print(f'Camera with id {camera_info["ip"]} was successfully saved')
    return {"status": "success"}


def create_camera_link():
    """
    Create link for each camera

    example -> http://admin-onvif:admin@192.168.1.160/onvif-http/snapshot?Profile_1
    """
    cameras_info = Camera.objects.all()
    result = []
    for camera_info in cameras_info:
        camera_data = {
            "ip": camera_info.id,
            "link": f"http://{camera_info.username}:{camera_info.password}@{camera_info.id}/onvif-http/snapshot?Profile_1",
        }
        result.append(camera_data)

    return result
