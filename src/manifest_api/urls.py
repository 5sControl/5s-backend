from django.urls import path
from rest_framework import routers
from src.manifest_api.views import ManifestConnectionViewSet, AssetClassesView, AssetsView, TemplateView

router = routers.DefaultRouter()
router.register(r'login', ManifestConnectionViewSet)

urlpatterns = [
    path('asset_classes/', AssetClassesView.as_view(), name='asset-classes'),
    path('assets/<int:asset_class_id>/', AssetsView.as_view(), name='asset'),
    path('templates/<int:asset_class_id>/', TemplateView.as_view(), name='template'),
]

urlpatterns += router.urls
