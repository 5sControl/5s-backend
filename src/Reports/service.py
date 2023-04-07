from src.MsSqlConnector.services import create_records
from src.OrderView.models import IndexOperations
from src.Reports.models import SkanyReport


def edit_extra(data):
    try:
        operation_index = IndexOperations.objects.first().type_operation
        skany_index = create_records.get_max_skany_indeks_by_typ(operation_index)
        data["skany_index"] = int(skany_index)
        print("skany_index", skany_index)
        print("type(skany_index)", type(skany_index))
    except Exception as e:
        print(f'failed to get skany index {e}')
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

