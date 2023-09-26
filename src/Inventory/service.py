from src.Inventory.models import Items

from src.Inventory.serializers import ItemsSerializer

from src.Mailer.message import send_email_to_suppliers
from src.Mailer.service import send_notification_email

from django.core.exceptions import ValidationError


def process_item_status(data):
    """Updates the item status and adds the status to the extra"""

    result = []
    data = data[0].get("items")
    for item_data in data:
        count = item_data["count"]
        red_line = item_data["low_stock_level"]
        data_item = Items.objects.filter(id=item_data["itemId"]).values(
            "current_stock_level", "low_stock_level", "status", "object_type"
        )
        min_item = data_item[0]["low_stock_level"]
        image_path = item_data["image_item"]
        level_previous_status = data_item[0]["status"]
        item = Items.objects.filter(id=item_data["itemId"]).first()

        item_serializer = ItemsSerializer(item)
        serialized_item = item_serializer.data

        if data_item[0]["object_type"] == "red line":
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
                        send_notification_email.apply_async(
                            args=[serialized_item, count, image_path, item_status],
                            countdown=0,
                        )
                    except Exception as e:
                        print(f"Email notification errors: {e}")

                    # send_notification suppliers
                    try:
                        item.prev_status = None
                        send_email_to_suppliers.apply_async(
                            args=[serialized_item, image_path]
                        )
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

            elif count > 0 and count <= min_item:
                item_status = "Low stock level"
                if level_previous_status == "In stock":
                    item.prev_status = "Low stock level"

                    # send_notification suppliers
                    try:
                        item.prev_status = None
                        send_email_to_suppliers.apply_async(
                            args=[serialized_item, image_path]
                        )
                    except Exception as e:
                        print(f"Email notification errors: {e}")

                    # send_notification
                    try:
                        item.prev_status = None
                        send_notification_email.apply_async(
                            args=[serialized_item, count, image_path, item_status],
                            countdown=0,
                        )
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
            f"red_line == {red_line}, item_type == {data_item[0]['object_type']}"
        )

        item.status = item_status
        item.save()

        item_data["status"] = item_status
        item_data["red_line"] = red_line

        result.append(item_data)
    return result


def is_valid_coordinates(coords):
    valid_coords = []

    for coord in coords:
        if (
            coord["x1"] > 0
            and coord["x2"] > 0
            and coord["y1"] > 0
            and coord["y2"] > 0
        ):
            area = (coord["x2"] - coord["x1"]) * (coord["y2"] - coord["y1"])
            if area > 250:
                valid_coords.append(coord)
    if len(valid_coords) == 0:
        raise ValidationError("Invalid size based on coords")
    return valid_coords





