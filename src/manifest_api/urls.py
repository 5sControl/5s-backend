from django.urls import path
from rest_framework import routers
from src.manifest_api.views import AssetClassesView, AssetsView, TemplateView, StepsView

router = routers.DefaultRouter()

urlpatterns = [
    path('asset_classes/', AssetClassesView.as_view(), name='asset-classes'),
    path('assets/<int:asset_class_id>/', AssetsView.as_view(), name='asset'),
    path('templates/<int:asset_class_id>/', TemplateView.as_view(), name='template'),
    path('steps/', StepsView.as_view(), name='steps'),
]

urlpatterns += router.urls
