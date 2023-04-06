from src.Inventory.models import Items

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
