import re
from django.db.models import Q
from datetime import datetime, timedelta

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

    result = [{"template_id": template_id, "name_workplace": data["name_workplace"], "steps": data["steps"]}
              for template_id, data in groups.items()]
    return result


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
    # filters all operations
    ## FiltrationOperationsTypeID.objects.filter(is_active=True)
    # only manifest
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


def get_jobs_manifest(data, from_date_str, to_date_str):
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(milliseconds=1)

    from_date_ms = int(from_date.timestamp() * 1000)
    to_date_ms = int(to_date.timestamp() * 1000)

    result = []
    operations = FiltrationOperationsTypeID.objects.filter(is_active=True)
    for operation in operations:
        oprs = []
        pattern = r'\.Step:\s*([^(]+)'

        match = re.search(pattern, operation.name)

        if match:
            operation_name = match.group(1).strip()
        else:
            operation_name = operation.name

        for job_step in data:
            if operation_name == job_step.get('job_step')[0].get('title'):
                if job_step.get('start_time'):
                    start_time = int(job_step.get('start_time'))
                else:
                    dt = datetime.strptime(job_step.get('created_at'), '%Y-%m-%dT%H:%M:%S.%fZ')
                    start_time = int(dt.timestamp() * 1000)
                    # test orders view
                # end_time = start_time + job_step.get('time') * 1000
                end_time = start_time + job_step.get('time') * 1000 * 20

                if from_date_ms <= start_time <= to_date_ms:
                    oprs.append(
                        {
                            "id": job_step.get('id'),
                            "orId": job_step.get('job_step_id'),
                            "sTime": start_time,
                            "eTime": end_time
                        },
                    )

        result.append({
            "oprTypeID": operation.operation_type_id,
            "oprName": operation.name,
            "oprs": oprs
        })
    return result
