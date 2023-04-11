from src.MsSqlConnector.services import create_records

from src.Reports.models import SkanyReport
from src.OrderView.models import IndexOperations


def edit_extra(data, camera):
    # try:
    print('print data extra', data)
    operation_index = IndexOperations.objects.filter(camera=camera.id).values('type_operation').last()[
        'type_operation']
    skany_index = create_records.get_max_skany_indeks_by_stanowisko(operation_index)
    data[0]["skany_index"] = int(skany_index)
    print("skany_index", data)
    # except Exception as e:
    #     print(f'failed to get skany index {e}')
    if len(data) <= 1:
        data.append({"skany_index": None})
    return data


def create_records_skany(report, skany):
    """
    save skany index and report in database
    """
    if skany[0].get('skany_index'):
        SkanyReport.objects.create(report=report, skany_index=skany['skany_index'])
    else:
        SkanyReport.objects.create(report=report)
