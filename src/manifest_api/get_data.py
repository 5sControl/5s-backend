import requests
from src.manifest_api.models import ManifestConnection


def get_asset_classes(query):
    manifest = ManifestConnection.objects.last()
    host = manifest.host
    token = manifest.token
    url = f"{host}graphql/v3"

    data_query = {
        "asset": "{\"query\":\"query(\\n  $assetClassId: Int, \\n  $locationId: Int, \\n  $maintRequired: Boolean, \\n  $outOfToleranceRange: Boolean\\n) {\\n  assets(\\n    assetClassId: $assetClassId, \\n    locationId: $locationId, \\n    maintRequired: $maintRequired, \\n    outOfToleranceRange: $outOfToleranceRange\\n  ) {\\n    assetClassId\\n    assets {\\n      id\\n      assetClassId\\n      locationId\\n      serialNumber\\n      internalId\\n      department\\n      criticality\\n      status\\n      assetTagId\\n      latitude\\n      longitude\\n      altitude\\n      assetClass {\\n        model\\n        make\\n        models {\\n          id\\n          name\\n          modelRotation\\n          isDefault\\n          modelOffset\\n          modelScale\\n          modelFiles {\\n            id\\n            name\\n            originalName\\n            url\\n            fileType\\n            contentType\\n            type\\n          }\\n        }\\n      }\\n      createdBy {\\n        id\\n        firstName\\n        lastName\\n        avatarDetails {\\n          id\\n          url\\n        }\\n        isOnline\\n      }\\n      updatedBy {\\n        id\\n        firstName\\n        lastName\\n        avatarDetails {\\n          id\\n          url\\n        }\\n        isOnline\\n      }\\n      location {\\n        name\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":{}}",
        "asset_class": "{\"query\":\"query(\\n  $assetClassId: Int, \\n  $locationId: Int, \\n  $maintRequired: Boolean, \\n  $outOfToleranceRange: Boolean\\n) {\\n  assets(\\n    assetClassId: $assetClassId, \\n    locationId: $locationId, \\n    maintRequired: $maintRequired, \\n    outOfToleranceRange: $outOfToleranceRange\\n  ) {\\n    assetClassId\\n    assets {\\n      id\\n      assetClassId\\n      locationId\\n      serialNumber\\n      internalId\\n      department\\n      criticality\\n      status\\n      assetTagId\\n      latitude\\n      longitude\\n      altitude\\n      assetClass {\\n        model\\n        make\\n        models {\\n          id\\n          name\\n          modelRotation\\n          isDefault\\n          modelOffset\\n          modelScale\\n          modelFiles {\\n            id\\n            name\\n            originalName\\n            url\\n            fileType\\n            contentType\\n            type\\n          }\\n        }\\n      }\\n      createdBy {\\n        id\\n        firstName\\n        lastName\\n        avatarDetails {\\n          id\\n          url\\n        }\\n        isOnline\\n      }\\n      updatedBy {\\n        id\\n        firstName\\n        lastName\\n        avatarDetails {\\n          id\\n          url\\n        }\\n        isOnline\\n      }\\n      location {\\n        name\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":{}}"
    }

    payload = data_query.get(query)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token,
        'User-Agent': 'PostmanRuntime/7.37.3',
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data = (response.json())
        return data
    except requests.exceptions.RequestException as e:
        raise ValueError({'error': str(e)})
