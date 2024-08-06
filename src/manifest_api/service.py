from src.CameraAlgorithms.models.camera import ZoneCameras
from src.Reports.models import Report
from src.Reports.serializers import ReportSerializersForManifest
from src.manifest_api.get_data import get_steps_by_asset_class

from django.db.models import Q
from datetime import datetime

from src.newOrderView.models import FiltrationOperationsTypeID


def adding_data_to_extra(extra):
    data = []

    for item in extra:

        try:
            zone = ZoneCameras.objects.get(id=item.get('zone_id'))
        except:
            zone = None

        if zone:
            item["id_workplace"] = zone.index_workplace
            item["name_workplace"] = zone.workplace
        data.append(item)
    return data


def edit_response_for_orders(data):
    result = []
    operations_map = set()

    operations = FiltrationOperationsTypeID.objects.filter(is_active=True)
    for item in operations:
        operation_tuple = (item.id, item.name, item.operation_type_id)
        operations_map.add(operation_tuple)

    all_operations = [{"oprTypeID": opr_type_id, "oprName": opr_name, "operation_type_id": operation_type_id} for opr_type_id, opr_name, operation_type_id in operations_map]

    for operation in all_operations:
        oprs = []

        for ordered_dict in data:
            id_value = ordered_dict.get('id')
            extra_value = ordered_dict.get('extra')
            for report in extra_value:
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

    for ids in steps_id:
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
