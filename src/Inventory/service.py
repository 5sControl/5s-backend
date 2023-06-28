from src.CameraAlgorithms.models import CameraAlgorithm, Algorithm, ZoneCameras
from src.Inventory.models import Items

from src.Core.const import SERVER_URL

from src.CameraAlgorithms.services.cameraalgorithm import camera_rtsp_link, send_run_request, stop_camera_algorithm, \
    update_status_algorithm
from src.Inventory.serializers import ItemsSerializer

from src.Mailer.message import send_email_to_suppliers

from src.Mailer.service import send_notification_email

from django.db.models import Q


def process_item_status(data):
    """Updates the item status and adds the status to the extra"""

    result = []
    data = data[0].get('items')
    for item_data in data:

        count = item_data['count']
        red_line = item_data['low_stock_level']
        data_item = Items.objects.filter(id=item_data['itemId']).values('current_stock_level', 'low_stock_level',
                                                                        'status', 'multi_row')
        min_item = data_item[0]['low_stock_level']
        image_path = item_data['image_item']
        level_previous_status = data_item[0]['status']
        item = Items.objects.filter(id=item_data['itemId']).first()

        item_serializer = ItemsSerializer(item)
        serialized_item = item_serializer.data

        if data_item[0]['multi_row']:

            if red_line:
                item_status = "Low stock level"
                if min_item == 0:
                    item.current_stock_level = 0
                    item_data["count"] = 0
                else:
                    item.current_stock_level = min_item - 1
                    item_data["count"] = min_item - 1

                if item.prev_status == "In stock":

                    # send_notification
                    try:
                        item.prev_status = None
                        send_notification_email.apply_async(args=[serialized_item, count, image_path, item_status],
                                                            countdown=0)
                    except Exception as e:
                        print(f"Email notification errors: {e}")

                    # send_notification suppliers
                    try:
                        item.prev_status = None
                        send_email_to_suppliers.apply_async(args=[serialized_item, image_path])
                    except Exception as e:
                        print(f"Email notification errors: {e}")

                item.prev_status = "Low stock level"

            else:
                item_status = "In stock"
                item.current_stock_level = min_item + 1
                item_data["count"] = min_item + 1
                item.prev_status = "In stock"

        else:
            if count == 0:
                item_status = "Out of stock"
                if item.prev_status == "Low stock level":
                    item.prev_status = None

                else:
                    if item.prev_status != None:
                        item.prev_status = item.status

            elif (count > 0 and count <= min_item):
                item_status = "Low stock level"
                if level_previous_status == "In stock":
                    item.prev_status = "Low stock level"

                    # send_notification suppliers
                    try:
                        item.prev_status = None
                        send_email_to_suppliers.apply_async(args=[serialized_item, image_path])
                    except Exception as e:
                        print(f"Email notification errors: {e}")

                    # send_notification
                    try:
                        item.prev_status = None
                        send_notification_email.apply_async(args=[serialized_item, count, image_path, item_status],
                                                            countdown=0)
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

        print(
            f"item_id=={item.id}, item_name=={item.name}, item_status {item_status}, "
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
        print("Stopped process algorithm MinMax", process_id)
        stop_camera_algorithm(pid=process_id)
        if not Items.objects.filter(camera_id=camera.id).exists():
            update_status_algorithm(pid=process_id)
        print("stopped process", camera)


def started_process(camera):
    """Started process algorithm MinMax"""

    camera_url = camera_rtsp_link(camera.id)
    algorithm = Algorithm.objects.get(name='min_max_control')
    algorithm_items = Items.objects.filter(camera=camera)
    data = []
    areas = []
    zones = []
    for item in algorithm_items:
        areas.append(
            {"itemId": item.id, "itemName": item.name, "coords": item.coords}
        )
    try:
        camera_algorithm = CameraAlgorithm.objects.get(
            Q(camera_id=camera) & Q(algorithm__name='min_max_control')
        )

        for zone_id in camera_algorithm.zones:
            zone_camera = ZoneCameras.objects.get(id=zone_id["id"], camera=camera)

            zones.append(
                {"zoneId": zone_camera.id, "zoneName": zone_camera.name, "coords": zone_camera.coords}
            )
    except:
        print("NO ZONE")

    data.append({
        "areas": areas,
        "zones": zones
    })

    new_data = {
        "camera_url": camera_url,
        "algorithm": algorithm.name,
        "server_url": SERVER_URL,
        "extra": data
    }

    try:
        response = send_run_request(new_data)

        new_process_id = response["pid"]
        print('new_process_id = response["pid"]', new_process_id)
        CameraAlgorithm.objects.create(camera=camera, algorithm=algorithm, process_id=new_process_id)

    except CameraAlgorithm.DoesNotExist:
        print("first algorithm not found")
        if len(data.get("extra")) == 0:
            return

        response = send_run_request(data)
        CameraAlgorithm.objects.create(algorithm=algorithm, camera=camera, process_id=response["pid"])

    print("started process", camera_url)
