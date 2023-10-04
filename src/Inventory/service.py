import logging
from src.Inventory.models import Items

from src.Inventory.serializers import ItemsSerializer

from src.Mailer.message import send_email_to_suppliers
from src.Mailer.service import send_notification_email

from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def process_item_status(data):
    """Updates the status of an item and adds it to the result."""
    result = []
    items_data = data[0].get("items")
    for item_data in items_data:
        item_id = item_data["itemId"]
        count = item_data["count"]
        image_path = item_data["image_item"]
        low_stock_level = item_data["low_stock_level"]

        item = Items.objects.filter(id=item_id).first()

        if item:
            process_item(item, count, image_path, low_stock_level)
            result.append(item_data)

    return result


def process_item(item, count, image_path, low_stock_level):
    """Handles item status."""
    result = []

    item_serializer = ItemsSerializer(item)
    serialized_item = item_serializer.data

    if serialized_item["object_type"] == "red line":
        if low_stock_level:
            item_status = "Low stock level"
            if serialized_item["low_stock_level"] == 0:
                item.current_stock_level = 0
                count = 0
            else:
                item.current_stock_level = serialized_item["low_stock_level"] - 1
                count = serialized_item["low_stock_level"] - 1

            if item.prev_status == "In stock":
                # send_notification Low stock level
                try:
                    item.prev_status = None
                    send_notification_email.apply_async(
                        args=[serialized_item, count, image_path, item_status],
                        countdown=0,
                    )
                except Exception as e:
                    print(f"Email notification errors: {e}")

                # send_notification suppliers Low stock level
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
            item.current_stock_level = serialized_item["low_stock_level"] + 1
            count = serialized_item["low_stock_level"] + 1
            item.prev_status = "In stock"

    else:
        if count == 0:
            item_status = "Out of stock"
            if item.prev_status == "Low stock level":
                item.prev_status = None
                # send_notification Out of stock
                try:
                    item.prev_status = None
                    send_notification_email.apply_async(
                        args=[serialized_item, count, image_path, item_status],
                        countdown=0,
                    )
                except Exception as e:
                    print(f"Email notification errors: {e}")

            else:
                if item.prev_status is not None:
                    item.prev_status = item.status

        elif 0 < count <= serialized_item["low_stock_level"]:
            item_status = "Low stock level"
            if serialized_item["status"] == "In stock":
                item.prev_status = "Low stock level"

                # send_notification suppliers Low stock level
                try:
                    item.prev_status = None
                    send_email_to_suppliers.apply_async(
                        args=[serialized_item, image_path]
                    )
                except Exception as e:
                    print(f"Email notification errors: {e}")

                # send_notification Low stock level
                try:
                    item.prev_status = None
                    send_notification_email.apply_async(
                        args=[serialized_item, count, image_path, item_status],
                        countdown=0,
                    )
                except Exception as e:
                    print(f"Email notification errors: {e}")
            elif item.prev_status is not None:
                item.prev_status = serialized_item["status"]

        else:
            item_status = "In stock"
            if item.prev_status is None:
                item.prev_status = "In stock"
            else:
                item.prev_status = serialized_item["status"]
        item.current_stock_level = count
        serialized_item["low_stock_level"] = serialized_item["low_stock_level"]

    print(
        f"item_id=={item.id}, item_name=={item.name}, item_status {item_status}, "
        f"low_stock_level == {low_stock_level}, item_type == {serialized_item['object_type']}"
    )

    item.status = item_status
    item.save()

    serialized_item["status"] = item_status
    serialized_item["low_stock_level"] = low_stock_level

    result.append(serialized_item)

    return result


def is_valid_coordinates(coords, type_object):
    size_coord = {"item": 250, "zone": 500}
    valid_coords = []

    for coord in coords:
        if (
            coord["x1"] > 0
            and coord["x2"] > 0
            and coord["y1"] > 0
            and coord["y2"] > 0
        ):
            area = (coord["x2"] - coord["x1"]) * (coord["y2"] - coord["y1"])
            if area > size_coord[f"{type_object}"]:
                valid_coords.append(coord)
    if len(valid_coords) == 0:
        logger.warning(f"There are no positive coordinates for the {type_object}:", coords)
        raise ValidationError("Invalid size based on coords")
    return valid_coords
