from src.MsSqlConnector.services import create_records


def edit_extra(data):
    try:
        skany_index = create_records.get_max_skany_indeks_by_typ(2)
        data["skany_index"] = skany_index
    except Exception as e:
        print(f'failed to get skany index {e}')

    return data

