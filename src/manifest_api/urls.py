from django.urls import path
from rest_framework import routers
from src.manifest_api.views import ManifestConnectionViewSet, AssetClassesView

router = routers.DefaultRouter()
router.register(r'login', ManifestConnectionViewSet)

urlpatterns = [
    path('asset_classes/', AssetClassesView.as_view(), name='asset-classes'),
]

urlpatterns += router.urls
