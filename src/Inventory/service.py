from src.Algorithms.models import CameraAlgorithm, Algorithm
from src.Cameras.models import Camera
from src.Inventory.models import Items
from django.db.models import Q
from src.Algorithms.service import algorithms_services

# from src.Mailer.service import send_message


def process_item_status(data):
    """Updates the item status and adds the status to the extra"""

    result = []

    for item_data in data:

        count = item_data['count']
        data_item = Items.objects.filter(id=item_data['itemId']).values('current_stock_level', 'low_stock_level')
        min_item = data_item[0]['low_stock_level']

        if count == 0:
            item_status = "Out of stock"
        elif count > 0 and count < min_item:
            item_status = "Low stock level"
            # send_message(data_item.values(), count)
        else:
            item_status = "In stock"

        item = Items.objects.filter(id=item_data['itemId']).first()
        item.status = item_status
        item.current_stock_level = count
        item.save()

        item_data["status"] = item_status
        item_data["low_stock_level"] = min_item

        result.append(item_data)

    return result


# def stop_all_items_algorithm():
#     """stop algorithm"""
#     cameras_items = Items.objects.values_list('camera__name', flat=True).distinct()
#     for camera in cameras_items:
#         from src.Algorithms.utils import yolo_proccesing
#         process_id = CameraAlgorithm.objects.filter(
#             Q(camera_id=camera) & Q(algorithm__name='min_max_control')
#         ).values_list('process_id', flat=True).first()
#         if process_id is not None:
#             yolo_proccesing.stop_process(pid=process_id)
#             algorithms_services.update_status_of_algorithm_by_pid(pid=process_id)
#     return start_all_items_algorithm(cameras_items)
#
#
# def start_all_items_algorithm(cameras_items):
#     """start process"""
#     for camera_data in cameras_items:
#
#         algorithm = Algorithm.objects.filter(name='min_max_control')
#         camera = Camera.objects.first(camera_data)
#
#         data = []
#         from src.Algorithms.utils import yolo_proccesing
#         server_url = yolo_proccesing.get_algorithm_url()
#         algorithm_items = Items.objects.filter(camera=camera_data)
#         print("algo items", algorithm_items.values())
#
#         for item in algorithm_items:
#             data.append({"itemId": item.id, "coords": item.coords})
#             print(f"coords: {item.coords}\nid {item.id}")
#         print(f"camera id: {camera_data}")
#
#         if len(data) == 0:
#             data = None
#         result = yolo_proccesing.start_yolo_processing(camera=camera, algorithm=algorithm[0], url=server_url, data=data)
#         print("result", result)
#     return