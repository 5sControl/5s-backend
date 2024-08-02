from src.CameraAlgorithms.models.camera import ZoneCameras
from src.Reports.models import Report
from src.Reports.serializers import ReportSerializers
from src.manifest_api.get_data import get_steps_by_asset_class

from django.db.models import Q
from datetime import datetime


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

    serializer = ReportSerializers(final_queryset, many=True)
    return serializer.data
