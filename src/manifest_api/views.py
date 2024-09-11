from rest_framework.views import APIView
from rest_framework.response import Response

from src.manifest_api.get_data import get_asset_classes, get_steps_by_asset_class


class AssetClassesView(APIView):
    def get(self, request):
        data, status_code = get_asset_classes(query="asset_class")
        return Response(data, status=status_code)


class AssetsView(APIView):
    def get(self, request, asset_class_id):
        data, status_code = get_asset_classes(query="asset", asset_class_id=asset_class_id)
        return Response(data, status=status_code)


class TemplateView(APIView):
    def get(self, request, asset_class_id):
        data, status_code = get_asset_classes(query="template", asset_class_id=asset_class_id)
        return Response(data, status=status_code)


class StepsView(APIView):
    def get(self, request):
        data, status_code = get_steps_by_asset_class()
        return Response(data, status=status_code)
