import requests
from datetime import datetime, timezone

from django.http import JsonResponse

from src.DatabaseConnections.models import ConnectionInfo
from src.newOrderView.models import FiltrationOperationsTypeID


def authenticate_user(host, database, username, password):
    session = requests.Session()

    response = session.get(f"{host}/web/login")
    if response.status_code != 200:
        raise ValueError(f"Error receiving CSRF token: {response.status_code}")

    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": database,
            "login": username,
            "password": password,
        },
        "id": 1,
    }
    headers = {
        'Content-Type': 'application/json',
        'X-CSRF-Token': session.cookies.get('csrf_token')
    }

    response = session.post(f"{host}/web/session/authenticate", json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        return session, response_data.get('result', {}).get('uid')
    else:
        raise ValueError(f"Authorization error: {response.status_code} - {response.text}")


def odoo_login():

    connection = ConnectionInfo.objects.filter(is_active=True, erp_system="odoo").first()
    url = connection.host
    db = connection.database
    username = connection.username
    password = connection.password

    user_id = authenticate_user(url, db, username, password)

    if user_id:
        return JsonResponse({"success": True, "user_id": user_id}, status=200)
    else:
        return JsonResponse({"success": False, "error": "Invalid credentials"}, status=403)


def odoo_get_data(table_name, fields=["id", "name"]):
    connection = ConnectionInfo.objects.filter(is_active=True, erp_system="odoo").first()
    url = connection.host
    db = connection.database
    username = connection.username
    password = connection.password

    session, user_id = authenticate_user(url, db, username, password)

    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                db,
                user_id,
                password,
                table_name,
                'search_read',
                [[('create_uid', '=', user_id)]],
                {
                    "fields": fields,
                    'order': 'write_date desc'
                }
            ]
        },
        "id": 2
    }

    response = session.post(f"{url}/jsonrpc", json=data)

    if response.status_code == 200:
        response_data = response.json().get('result', [])
        return response_data, response.status_code
    else:
        raise ValueError(f"Error fetching data: {response.status_code} - {response.text}")


def edit_answer_from_odoo(data):
    for item in data:
        item['name'] = item.pop('display_name')
    return data


def convert_to_milliseconds(date_string):
    try:
        date_format = '%Y-%m-%d %H:%M:%S'
        naive_datetime = datetime.strptime(date_string, date_format)
        milliseconds = int(naive_datetime.timestamp() * 1000)
        return milliseconds
    except:
        return None


def sorted_data_odoo(data, type_operation):
    result = []

    if type_operation == 'orders':
        for orders in data:
            duration = 0
            duration_expected = 0

            for order in orders.get("workorders", []):
                order_duration = order.get("duration") or 0.0
                order_duration_expected = order.get("duration_expected") or 0.0

                duration += (order_duration * 60)
                duration_expected += (order_duration_expected * 60)

            result.append(
                {
                    "orId": orders.get('production_name'),
                    "duration": duration * 1000,
                    "duration_expected": duration_expected * 1000
                }
            )

    else:
        operations = FiltrationOperationsTypeID.objects.filter(is_active=True, type_erp="odoo")
        for operation in operations:
            oprs = []
            for orders in data:
                order_id = orders.get('production_name')
                data_operations = orders.get("workorders")
                for data_operation in data_operations:
                    if data_operation.get('name') == operation.name:
                        start_time = convert_to_milliseconds(data_operation.get('date_start'))
                        end_time = convert_to_milliseconds(data_operation.get('date_finished'))
                        duration = data_operation.get('duration') * 60 * 1000
                        duration_expected = data_operation.get('duration_expected') * 60 * 1000
                        oprs.append(
                            {
                                "id": data_operation.get('id'),
                                "orId": order_id,
                                "sTime": start_time,
                                "eTime": end_time,
                                "duration": duration,
                                "duration_expected": duration_expected
                            },
                        )

            result.append({
                "filtration_operation_id": operation.id,
                "oprTypeID": operation.operation_type_id,
                "oprName": operation.name,
                "oprs": oprs
            })
    if type_operation != 'orders':
        sorted_data = sorted(result, key=lambda x: x["filtration_operation_id"])
        return sorted_data

    return result


def get_all_order_odoo(from_date, to_date):
    connection = ConnectionInfo.objects.filter(is_active=True, erp_system="odoo").first()
    url = connection.host
    db = connection.database
    username = connection.username
    password = connection.password

    session, user_id = authenticate_user(url, db, username, password)

    if not session or not user_id:
        print("Failed to authenticate user.")
        return []

    # Basic request for production
    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                db,
                user_id,
                password,
                'mrp.production',
                'search_read',
                [[('create_uid', '=', user_id),
                  ('date_start', '>=', from_date),
                  ('date_start', '<=', to_date),
                  ('state', '=', 'done')]],
                {
                    "fields": ["id", 'name', 'workorder_ids'],
                }
            ]
        },
        "id": 1
    }

    try:
        response = session.post(url + '/jsonrpc', json=data)
        response.raise_for_status()
        productions = response.json().get('result', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching productions: {e}")
        return []

    if productions:
        orders_with_workorders = []

        for production in productions:
            production_info = {
                'production_id': production['id'],
                'production_name': production['name'],
                'workorders': []
            }

            if production['workorder_ids']:
                # Request for information on workorders
                workorder_data = {
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "object",
                        "method": "execute_kw",
                        "args": [
                            db,
                            user_id,
                            password,
                            'mrp.workorder',
                            'search_read',
                            [[('id', 'in', production['workorder_ids'])]],
                            {
                                "fields": ['id', 'name', 'date_start', 'date_finished', 'duration', "duration_expected"]
                            }
                        ]
                    },
                    "id": production['id']
                }

                try:
                    workorder_response = session.post(url + '/jsonrpc', json=workorder_data)
                    workorder_response.raise_for_status()
                    workorders = workorder_response.json().get('result', [])
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching workorders for production {production['id']}: {e}")
                    workorders = []

                production_info['workorders'] = workorders

            orders_with_workorders.append(production_info)

        return orders_with_workorders

    else:
        print("No productions found.")
        return []


def details_for_operation(order_id):
    connection = ConnectionInfo.objects.filter(is_active=True, erp_system="odoo").first()
    url = connection.host
    db = connection.database
    username = connection.username
    password = connection.password

    session, user_id = authenticate_user(url, db, username, password)

    if not session or not user_id:
        print("Failed to authenticate user.")
        return []

    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                db,
                user_id,
                password,
                'mrp.workorder',
                'search_read',
                [[('id', '=', order_id)]],
                {
                    "fields": [],
                }
            ]
        },
        "id": 1
    }

    response = session.post(url + '/jsonrpc', json=data)
    response.raise_for_status()
    operation = response.json().get('result', [])[0]
    id_order = operation.get("production_id")[0]
    start_time = convert_to_milliseconds(operation.get('date_start'))
    end_time = convert_to_milliseconds(operation.get('date_finished'))

    link = f"{url}web#id={id_order}&cids=1&menu_id=320&action=540&model=mrp.production&view_type=form"
    result = {
        "id": operation.get("id"),
        "orId": id_order,
        "oprName": operation.get("display_name"),
        "url": link,
        # "elType": elementType,
        "sTime": start_time,
        "eTime": end_time,
        # "frsName": firstName,
        # "lstName": lastName,
        "status": operation.get("state"),
        "video": False
        # "video": get_skany_video_info(time, ip_camera),
    }

    return result
