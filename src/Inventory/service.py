from src.Algorithms.models import CameraAlgorithm
from src.Algorithms.utils import yolo_proccesing
from src.Inventory.models import Items
from src.Cameras.models import Camera
from src.Algorithms.models import Algorithm

from src.Mailer.service import send_email

from django.db.models import Q


def process_item_status(data):
    """Updates the item status and adds the status to the extra"""

    result = []

    for item_data in data:

        count = item_data['count']
        red_line = item_data['low_stock_level']
        data_item = Items.objects.filter(id=item_data['itemId']).values('current_stock_level', 'low_stock_level',
                                                                        'status', 'multi_row')
        min_item = data_item[0]['low_stock_level']
        image_path = item_data['image_item']
        level_previous_status = data_item[0]['status']
        item = Items.objects.filter(id=item_data['itemId']).first()

        if count == 0:
            item_status = "Out of stock"
            if item.prev_status == "Low stock level":
                try:
                    item.prev_status = None
                    send_email(item, image_path, count, item_status)
                except Exception as e:
                    print(f"Email notification errors: {e}")
            else:
                if item.prev_status != None:
                    item.prev_status = item.status

        elif (count > 0 and count <= min_item) or red_line == True and data_item[0]['multi_row']:
            item_status = "Low stock level"
            if level_previous_status == "In stock":
                previous_status = "Low stock level"
                try:
                    send_email(item, image_path, count, item_status)
                except Exception as e:
                    print(f"Email notification errors: {e}")
            elif item.prev_status != None:
                item.prev_status = item.status

        else:
            item_status = "In stock"
            if item.prev_status == None:
                item.prev_status = "In stock"
            else:
                item.prev_status = item.status

        if data_item[0]['multi_row']:
            print("red_line", red_line)
            if red_line:

                item_status = "low_stock_level"
            else:
                item_status = "In stock"

            item.current_stock_level = count
        print("item_status", item_status)
        item.status = item_status
        item.save()

        item_data["status"] = item_status
        item_data["low_stock_level"] = min_item

        result.append(item_data)

    return result


def stopped_process(camera):
    """Stopped process algorithm MinMax"""
    from src.Algorithms.service import algorithms_services
    process_id = CameraAlgorithm.objects.filter(
        Q(camera_id=camera) & Q(algorithm__name='min_max_control')
    ).values_list('process_id', flat=True).first()
    if process_id is not None:
        yolo_proccesing.stop_process(pid=process_id)
        algorithms_services.update_status_of_algorithm_by_pid(pid=process_id)
        print("stopped process", camera)


def started_process(camera_item):
    """Started process algorithm MinMax"""
    from src.Algorithms.service import algorithms_services
    # started process
    camera = Camera.objects.filter(id=camera_item)
    algorithm = Algorithm.objects.filter(name='min_max_control')
    algorithms_services.create_new_records(cameras=camera, algorithm=algorithm[0])
    print("started process", camera)
