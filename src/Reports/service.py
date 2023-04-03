from src.MsSqlConnector.services import create_records
from src.Reports.models import SkanyReport


def edit_extra(data):
    try:
        skany_index = create_records.get_max_skany_indeks_by_typ(2)
        data["skany_index"] = skany_index
    except Exception as e:
        print(f'failed to get skany index {e}')

    return data


def create_records_skany(report, skany):
    """
    save skany index and report in database
    """
    if skany.get('skany_index'):
        SkanyReport.objects.create(report=report, skany_index=skany['skany_index'])
    else:
        SkanyReport.objects.create(report=report)
    return


def get_skany_indexes(status=None):
    """
    Returns a list of SkanyReport skany_index values for all reports.
    """
    skany_indexes = SkanyReport.objects.filter(report__violation_found=status).values_list('skany_index', flat=True)
    return list(skany_indexes)
