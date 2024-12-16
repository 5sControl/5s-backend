import re
from src.CameraAlgorithms.models.camera import ZoneCameras
from src.DatabaseConnections.models import ConnectionInfo
from src.newOrderView.models import FiltrationOperationsTypeID


def adding_data_to_extra(extra):
    duration_zones = extra[-1].get('duration_zones', [])
    data = []

    for item in duration_zones:

        try:
            zone = ZoneCameras.objects.get(id=item.get('zone_id'))
        except:
            zone = None

        if zone:
            item["id_workplace"] = zone.index_workplace
            item["name_workplace"] = zone.workplace
        data.append(item)
    return data


def sorted_response(extra):
    try:
        groups = {}

        for item in extra:
            name_workplace = item.get('name_workplace')
            zone_id = item.get('zone_id')
            id_workplace = item.get('id_workplace')
            start_time = item.get('start_time')
            all_durations = item.get('all_durations')
            all_images_zones = item.get("all_images_zones")

            template_match = re.search(r'Template:.*\((\d+)\)', name_workplace)
            step_match = re.search(r'\.Step:.*\((Step\d+)\)', name_workplace)

            if template_match:
                template_id = int(template_match.group(1))
                if step_match:
                    step_id = int(re.search(r'Step(\d+)', step_match.group(1)).group(1))
                else:
                    step_id = 1

                if template_id not in groups:
                    groups[template_id] = {
                        "name_workplace": name_workplace,
                        "steps": []
                    }

                groups[template_id]["steps"].append(
                    {
                        "zone_id": zone_id,
                        "step": step_id,
                        "id_workplace": id_workplace,
                        "start_time": start_time,
                        "all_durations": all_durations,
                        "all_images_zones": all_images_zones
                    }
                )

        for data in groups.values():
            data["steps"].sort(key=lambda x: x["step"])

        result = [{"template_id": template_id, "name_workplace": data["name_workplace"], "steps": data["steps"]}
                  for template_id, data in groups.items()]

        return result

    except Exception as e:
        print(f"Exception error for sorted_response sender manifest: {e}")
        return None


def extract_name_operations(text):
    pattern = r'Template:\s*(.*?)\s*\(.*?\)\.\s*Step:\s*(.*?)\s*\(.*?\)'
    matches = re.search(pattern, text)

    if matches:
        template_value = matches.group(1)
        step_value = matches.group(2)
        return f"{template_value}, {step_value}"
    else:
        return text


def get_objects_operations(data, name_operations):
    for item in data:
        if item.get('operationName') == name_operations:
            return item


def sum_durations_by_or_id(data):
    result = []

    for order in data:
        order_job = order.get('orders_jobs')
        durations = 0

        for job in order_job:
            durations += int(job.get('jobs')[0].get("job_step")[0].get("job_step_ext")[0].get("duration"))

        result.append(
                {
                    "orId": order.get('id'),
                    "duration": durations * 1000
                }
            )
    return result


def get_jobs_manifest(data, type_operations):
    result = []

    connection = ConnectionInfo.objects.filter(used_in_orders_view=True).first()
    typ_erp = connection.erp_system
    operations = FiltrationOperationsTypeID.objects.filter(type_erp=typ_erp)
    for operation in operations:
        if type_operations == 'orders':
            return sum_durations_by_or_id(data)

        oprs = []
        for orders in data:
            order_id = orders.get('id')
            for job_order in orders.get('orders_jobs'):
                job = job_order.get('jobs')[0]
                job_step = job.get('job_step')[0].get('step')
                job_step_id = job.get('job_step')[0].get('id')
                job_step_name = job.get('job_step')[0].get('title')

                asset_id = job_order.get('jobs')[0].get('assets')[0].get('id')
                asset_name = job_order.get('jobs')[0].get('assets')[0].get('serial_number')
                template_id = job_order.get('jobs')[0].get('templates')[0].get('id')
                template_name = job_order.get('jobs')[0].get('templates')[0].get('title')
                job_step_operation_name = f"Asset: {asset_name}({asset_id}). Template: {template_name}({template_id}).Step: {job_step_name}(Step{job_step})"
                if operation.name == job_step_operation_name:
                    start_time = int(job_order.get('jobs')[0].get("job_step")[0].get('job_step_ext')[0].get('start_time'))
                    end_time = start_time + int(job_order.get('jobs')[0].get("job_step")[0].get('job_step_ext')[0].get('duration')) * 1000
                    oprs.append(
                        {
                            "id": job_step_id,
                            "orId": order_id,
                            "sTime": start_time,
                            "eTime": end_time
                        },
                    )

        if type_operations != 'orders':
            result.append({
                "filtration_operation_id": operation.id,
                "oprTypeID": operation.operation_type_id,
                "oprName": extract_name_operations(operation.name),
                "oprs": oprs
            })
    if type_operations != 'orders':
        sorted_data = sorted(result, key=lambda x: x["filtration_operation_id"])

        return sorted_data
