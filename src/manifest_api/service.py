import re
from django.db.models import Q
from datetime import datetime, timedelta
from collections import defaultdict

from src.CameraAlgorithms.models.camera import ZoneCameras
from src.Reports.models import Report
from src.Reports.serializers import ReportSerializersForManifest
from src.manifest_api.get_data import get_steps_by_asset_class

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


def edit_response_for_orders(data):
    result = []
    operations_map = set()

    operations = FiltrationOperationsTypeID.objects.filter(is_active=True)
    for item in operations:
        operation_tuple = (item.id, item.name, item.operation_type_id)
        operations_map.add(operation_tuple)

    all_operations = [{"oprTypeID": opr_type_id, "oprName": opr_name,
                       "operation_type_id": operation_type_id}
                      for opr_type_id, opr_name, operation_type_id in operations_map]

    for operation in all_operations:
        oprs = []

        for ordered_dict in data:
            id_value = ordered_dict.get('id')
            extra_value = ordered_dict.get('extra')
            for report in extra_value:
                print(report.get("duration"))
                if report.get("id_workplace") == operation.get("operation_type_id"):
                    start_tile = int(datetime.strptime(report.get('date'), "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000)
                    end_time = start_tile + 600000
                    oprs.append(
                        {
                            "id": id_value,
                            "orId": f"{operation.get('operation_type_id')}",
                            "sTime": start_tile,
                            "eTime": end_time
                        },

                    )

        result.append({
            "oprTypeID": operation.get("oprTypeID"),
            "oprName": operation.get("oprName"),
            "oprs": oprs
        })

    sorted_result = sorted(result, key=lambda x: x["oprTypeID"], reverse=True)
    return sorted_result


def get_all_reports_manifest(from_date, to_date):
    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
    to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
    to_date_obj = to_date_obj.replace(hour=23, minute=59, second=59)

    all_steps = get_steps_by_asset_class()[0]
    steps_id = [item["id"] for item in all_steps]
    unique_reports = set()

    for ids in set(steps_id):
        if not ids:
            continue
        queryset = Report.objects.filter(
            Q(date_created__gte=from_date_obj),
            Q(date_created__lte=to_date_obj),
            Q(extra__contains=[{"id_workplace": ids}])
        ).order_by("-date_created", "-id")

        unique_reports.update(queryset.values_list('id', flat=True))

    final_queryset = Report.objects.filter(id__in=unique_reports).order_by("-date_created", "-id")

    serializer = ReportSerializersForManifest(final_queryset, many=True)

    result = edit_response_for_orders(serializer.data)
    return result


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
            durations += int(job.get("duration")[0].get("time"))

        result.append(
                {
                    "orId": order.get('id'),
                    "duration": durations * 1000
                }
            )
    return result


def get_jobs_manifest(data, type_operations):
    result = []
    operations = FiltrationOperationsTypeID.objects.filter(is_active=True)
    for operation in operations:
        if type_operations == 'orders':
            return sum_durations_by_or_id(data)

        oprs = []
        for orders in data:
            order_id = orders.get('id')
            for job_order in orders.get('orders_jobs'):
                job = job_order.get('duration')[0]
                job_step_id = job.get('job_step')[0].get('step')
                job_step_name = job.get('job_step')[0].get('title')
                asset_id = job_order.get('jobs')[0].get('assets')[0].get('id')
                asset_name = job_order.get('jobs')[0].get('assets')[0].get('serial_number')
                template_id = job_order.get('jobs')[0].get('templates')[0].get('id')
                template_name = job_order.get('jobs')[0].get('templates')[0].get('title')
                job_step_operation_name = f"Asset:{asset_name}({asset_id}). Template: {template_name}({template_id}).Step: {job_step_name}(Step{job_step_id})"
                if operation.name == job_step_operation_name:
                    start_time = int(job.get('start_time'))
                    end_time = start_time + int(job.get('time')) * 1000
                    oprs.append(
                        {
                            "id": job_order.get('job_step_id'),
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
