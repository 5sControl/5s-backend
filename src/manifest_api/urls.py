from django.urls import path
from rest_framework import routers
from src.manifest_api.views import ManifestConnectionViewSet, AssetClassesView, AssetsView

router = routers.DefaultRouter()
router.register(r'login', ManifestConnectionViewSet)

urlpatterns = [
    path('asset_classes/', AssetClassesView.as_view(), name='asset-classes'),
    path('all_assets/', AssetsView.as_view(), name='assets'),
]

urlpatterns += router.urls
