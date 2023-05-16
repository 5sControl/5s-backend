from src.CameraAlgorithms.models import CameraAlgorithm, Algorithm
from src.Inventory.models import Items
from src.CameraAlgorithms.services.cameraalgorithm import camera_rtsp_link, send_run_request, stop_camera_algorithm

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
        if data_item[0]['multi_row']:

            if red_line:
                item_status = "Low stock level"
                item.current_stock_level = min_item - 1
                item_data["count"] = min_item - 1
            else:
                item_status = "In stock"
                item.current_stock_level = min_item + 1
                item_data["count"] = min_item + 1
        else:
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
            item.current_stock_level = count
            item_data["low_stock_level"] = min_item

        print(f"item_id=={item.id}, item_status {item_status}, "
              f"red_line == {red_line}, multi_row == {data_item[0]['multi_row']}")
        item.status = item_status
        item.save()

        item_data["status"] = item_status
        item_data["red_line"] = red_line

        result.append(item_data)
    return result


def stopped_process(camera):
    """Stopped process algorithm MinMax"""
    process_id = CameraAlgorithm.objects.filter(
        Q(camera_id=camera) & Q(algorithm__name='min_max_control')
    ).values_list('process_id', flat=True).first()
    if process_id is not None:
        stop_camera_algorithm(pid=process_id)
        print("stopped process", camera)


def started_process(camera):
    """Started process algorithm MinMax"""

    camera_url = camera_rtsp_link(camera.id)
    algorithm = Algorithm.objects.get(name='min_max_control')
    algorithm_items = Items.objects.filter(camera=camera)

    extra = []
    for item in algorithm_items:
        extra.append(
            {
                "itemId": item.id,
                "coords": item.coords,
                "itemName": item.name,
            }
        )

    data = {
        "camera_url": camera_url,
        "algorithm": algorithm.name,
        "extra": extra
    }

    try:
        camera_algorithm = CameraAlgorithm.objects.get(
            Q(camera_id=camera) & Q(algorithm__name='min_max_control')
        )
        response = send_run_request(data)

        new_process_id = response["pid"]

        camera_algorithm.process_id = new_process_id
        camera_algorithm.save()
    except CameraAlgorithm.DoesNotExist:
        print("first algorithm not found")
        response = send_run_request(data)
        CameraAlgorithm.objects.create(algorithm=algorithm, camera=camera, process_id=response["pid"])

    print("started process", camera_url)
