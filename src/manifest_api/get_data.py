import json

import requests

from src.manifest_api.models import ManifestConnection


def send_request(payload):
    manifest = ManifestConnection.objects.last()
    host = manifest.host
    token = manifest.token
    url = f"{host}graphql/v3"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token,
        'User-Agent': 'PostmanRuntime/7.37.3',
    }

    response = None
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        return data, response.status_code
    except requests.exceptions.HTTPError as http_err:
        return {'error': f'HTTP error occurred: {http_err}'}, response.status_code
    except requests.exceptions.RequestException as req_err:
        return {'error': f'Request exception occurred: {req_err}'}, 400


def upload_file(file_path):
    manifest = ManifestConnection.objects.last()
    host = manifest.host
    token = manifest.token
    url = f"{host}graphql/v3?storage=manifest"

    file_name = file_path.split('/')[-1].split('.')[-2]

    payload = {
        'contentType': 'image',
        'name': file_name,
        'multiply': 'false'
    }

    with open(file_path, 'rb') as file:
        files = [
            ('file', (file_name, file, 'application/octet-stream'))
        ]

        headers = {
            'Authorization': token,
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.37.3',
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print("upload_file", response.status_code)
        print("upload_file", response.text)

        if response.status_code == 200:
            print(response.text)
            data = response.json()
            id_image = data.get('id')
            print("id_image", id_image)
            return {"id": id_image}
        else:
            return None


def get_asset_classes(query, **kwargs):
    manifest = ManifestConnection.objects.last()
    host = manifest.host
    token = manifest.token
    url = f"{host}graphql/v3"
    asset_class_id = None

    if query == "asset" or "template":
        asset_class_id = kwargs.get("asset_class_id")

    data_query = {
        "asset_class": "{\"query\":\"query($deleted: Boolean) {\\n  assetClasses(deleted: $deleted) {\\n    id\\n    name\\n    status\\n    createdAt\\n    createdAt\\n}\\n}\\n\",\"variables\":{\"deleted\":false}}",
        "asset": "{\"query\":\"query(\\n  $assetClassId: Int,\\n  $locationId: Int,\\n  $maintRequired: Boolean,\\n  $outOfToleranceRange: Boolean\\n) {\\n  assets(\\n    assetClassId: $assetClassId,\\n    locationId: $locationId,\\n    maintRequired: $maintRequired,\\n    outOfToleranceRange: $outOfToleranceRange\\n  ) {\\n    assetClassId\\n    assets {\\n      id\\n      internalId\\n      serialNumber\\n      locationId\\n      status\\n      department\\n      criticality\\n      history {\\n        id\\n        contributors {\\n          id\\n        }\\n      }\\n      vumarkGuid\\n      locationId\\n    }\\n  }\\n}\\n\",\"variables\":{\"assetClassId\": " + f"{asset_class_id}" + "}}",
        "template": "{\"query\":\"query(\\n  $itemsPerPage: Int\\n  $pageNumber: Int\\n  $filters: TemplateVersionsFiltersInput\\n  $orderBy: String\\n  $reverseOrder: Boolean\\n  $search: TemplateVersionSearchInput\\n  $sort: SortInput\\n) {\\n  allVersionsWithPagination(\\n    itemsPerPage: $itemsPerPage\\n    pageNumber: $pageNumber\\n    filters: $filters\\n    orderBy: $orderBy\\n    reverseOrder: $reverseOrder\\n    search: $search\\n    sort: $sort\\n  ) {\\n    id\\n    title\\n    createdAt\\n    assetClass {\\n      name\\n      id\\n    }\\n    author {\\n      id\\n    }\\n    customEvidence {\\n      id\\n      name\\n    }\\n    createdBy {\\n      firstName\\n      lastName\\n      avatarDetails {\\n        url\\n      }\\n    }\\n    steps {\\n        id\\n      step\\n      title\\n      noteTypesOrder\\n      requiredEvidence\\n      evidenceRequirements\\n      highlights {\\n        id\\n        position\\n        rotation\\n        type\\n        data\\n      }\\n      notes {\\n        autoplay\\n        id\\n        userId\\n        animationName\\n        modelViewId\\n        type\\n        meterRequirements {\\n          id\\n          value\\n          evaluationType\\n          meterId\\n        }\\n      }\\n    }\\n    actualVersion {\\n      id\\n      name\\n      state\\n      rootTemplateId\\n      templateId\\n      description\\n      activities {\\n        id\\n        action\\n        comment\\n        createdByUser {\\n          id\\n          firstName\\n          lastName\\n          avatarDetails {\\n            id\\n            url\\n          }\\n          isOnline\\n        }\\n        createdAt\\n      }\\n    }\\n    versions {\\n      id\\n      name\\n      state\\n      rootTemplateId\\n      description\\n      templateId\\n      activities {\\n        id\\n        action\\n        comment\\n        createdByUser {\\n          id\\n          firstName\\n          lastName\\n          avatarDetails {\\n            id\\n            url\\n          }\\n          isOnline\\n        }\\n        createdAt\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":{\"pageNumber\":null,\"itemsPerPage\":3,\"filters\":{\"asset_class_id\":[2685],\"type\":[],\"status\":[\"published\"]},\"search\":{},\"sort\":{\"propertyName\":\"id\",\"reverse\":true}}}"
    }

    payload = data_query.get(query)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token,
        'User-Agent': 'PostmanRuntime/7.37.3',
    }

    response = None
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        return data, response.status_code
    except requests.exceptions.HTTPError as http_err:
        return {'error': f'HTTP error occurred: {http_err}'}, response.status_code
    except requests.exceptions.RequestException as req_err:
        return {'error': f'Request exception occurred: {req_err}'}, 400


def get_all_assets():
    result = []
    payload = "{\"query\":\"query(\\n  $assetClassId: Int, \\n  $locationId: Int, \\n  $maintRequired: Boolean, \\n  $outOfToleranceRange: Boolean\\n) {\\n  assets(\\n    assetClassId: $assetClassId, \\n    locationId: $locationId, \\n    maintRequired: $maintRequired, \\n    outOfToleranceRange: $outOfToleranceRange\\n  ) {\\n    assetClassId\\n    assets {\\n      id\\n      assetClassId\\n      locationId\\n      serialNumber\\n      internalId\\n      department\\n      criticality\\n      status\\n      assetTagId\\n      latitude\\n      longitude\\n      altitude\\n      assetClass {\\n        model\\n        make\\n        models {\\n          id\\n          name\\n          modelRotation\\n          isDefault\\n          modelOffset\\n          modelScale\\n          modelFiles {\\n            id\\n            name\\n            originalName\\n            url\\n            fileType\\n            contentType\\n            type\\n          }\\n        }\\n      }\\n      createdBy {\\n        id\\n        firstName\\n        lastName\\n        avatarDetails {\\n          id\\n          url\\n        }\\n        isOnline\\n      }\\n      updatedBy {\\n        id\\n        firstName\\n        lastName\\n        avatarDetails {\\n          id\\n          url\\n        }\\n        isOnline\\n      }\\n      location {\\n        name\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":{}}"
    response, status_code = send_request(payload)
    if status_code != 200:
        return [], status_code
    asset_classes = response.get('data').get('assets')
    for assets in asset_classes:
        for asset in assets.get("assets"):
            result.append(
                {
                    "asset_class_id": asset.get("assetClassId"),
                    'id_asset': asset.get('id'),
                    "location_id": asset.get('locationId'),
                    "serial_number": asset.get('serialNumber'),
                 }
            )
    return result


def get_steps_by_asset_class():
    data = []
    payload = "{\"query\":\"query(\\n  $itemsPerPage: Int\\n  $pageNumber: Int\\n  $filters: TemplateVersionsFiltersInput\\n  $orderBy: String\\n  $reverseOrder: Boolean\\n  $search: TemplateVersionSearchInput\\n  $sort: SortInput\\n) {\\n  allVersionsWithPagination(\\n    itemsPerPage: $itemsPerPage\\n    pageNumber: $pageNumber\\n    filters: $filters\\n    orderBy: $orderBy\\n    reverseOrder: $reverseOrder\\n    search: $search\\n    sort: $sort\\n  ) {\\n    id\\n    title\\n    createdAt\\n    assetClass {\\n      name\\n      id\\n    }\\n    author {\\n      id\\n    }\\n    customEvidence {\\n      id\\n      name\\n    }\\n    createdBy {\\n      firstName\\n      lastName\\n      avatarDetails {\\n        url\\n      }\\n    }\\n    steps {\\n        id\\n      step\\n      title\\n      noteTypesOrder\\n      requiredEvidence\\n      evidenceRequirements\\n      highlights {\\n        id\\n        position\\n        rotation\\n        type\\n        data\\n      }\\n      notes {\\n        autoplay\\n        id\\n        userId\\n        animationName\\n        modelViewId\\n        type\\n        meterRequirements {\\n          id\\n          value\\n          evaluationType\\n          meterId\\n        }\\n      }\\n    }\\n    actualVersion {\\n      id\\n      name\\n      state\\n      rootTemplateId\\n      templateId\\n      description\\n      activities {\\n        id\\n        action\\n        comment\\n        createdByUser {\\n          id\\n          firstName\\n          lastName\\n          avatarDetails {\\n            id\\n            url\\n          }\\n          isOnline\\n        }\\n        createdAt\\n      }\\n    }\\n    versions {\\n      id\\n      name\\n      state\\n      rootTemplateId\\n      description\\n      templateId\\n      activities {\\n        id\\n        action\\n        comment\\n        createdByUser {\\n          id\\n          firstName\\n          lastName\\n          avatarDetails {\\n            id\\n            url\\n          }\\n          isOnline\\n        }\\n        createdAt\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":{\"pageNumber\":null,\"itemsPerPage\":3,\"filters\":{\"asset_class_id\":[],\"type\":[],\"status\":[\"published\"]},\"search\":{},\"sort\":{\"propertyName\":\"id\",\"reverse\":true}}}"

    response, status_code = send_request(payload)
    if status_code != 200:
        return [], status_code

    response_data = response.get('data')
    if response_data:
        all_assets = get_all_assets()
        all_data = response_data.get('allVersionsWithPagination', [])
        for asset in all_assets:
            for template in all_data:
                try:
                    creator_by_id = template.get('actualVersion').get('activities')[0].get('createdByUser').get('id')
                except:
                    creator_by_id = None
                asset_name = asset.get("serial_number")
                asset_id = asset.get("id_asset")
                steps = template.get('steps', [])
                data.append(
                    {
                        # "id": step.get("id"),
                        "id": None,
                        "operationName": f"{asset_name}({asset_id}){template.get('title')}({template.get('id')})",
                        "asset_class_id": asset.get("asset_class_id"),
                        "id_asset": asset_id,
                        "location_id": asset.get("location_id"),
                        "serial_number": asset_name,
                        "creator_by_id": creator_by_id
                    }
                )
                for step in steps:
                    result = (
                        {
                            "id": step.get("id"),
                            "operationName": f"{asset_name}({asset_id}){template.get('title')}({template.get('id')}).{step.get('title')}(Step{step.get('step')})",
                            "asset_class_id": asset.get("asset_class_id"),
                            "id_asset": asset_id,
                            "location_id": asset.get("location_id"),
                            "serial_number": asset_name,
                            "creator_by_id": creator_by_id
                        }
                    )
                    data.append(result)
        return data, status_code
