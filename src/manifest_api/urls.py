from rest_framework import routers
from src.manifest_api.views import ManifestConnectionViewSet

router = routers.DefaultRouter()
router.register(r'login', ManifestConnectionViewSet)

urlpatterns = []

urlpatterns += router.urls
