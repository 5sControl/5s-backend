from src.Inventory.models import Items


def process_item_status(data):
    """Updates the item status and adds the status to the extra"""

    item_data = data['itemId']
    count = data['count']
    data_item = Items.objects.filter(id=item_data).values('current_stock_level', 'low_stock_level')
    min_item = data_item[0].get('low_stock_level')

    if count == 0:
        item_status = "Out of stock"
    elif count > 0 and count < min_item:
        item_status = "Low stock level"
    else:
        item_status = "In stock"

    item = Items.objects.filter(id=item_data).first()
    item.status = item_status
    item.current_stock_level = count
    item.save()

    data["status"] = item_status
    data["low_stock_level"] = min_item

    return data
