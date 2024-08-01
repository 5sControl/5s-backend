from src.CameraAlgorithms.models.camera import ZoneCameras


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
