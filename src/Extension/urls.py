from rest_framework.routers import DefaultRouter
from src.Extension.views import ExtensionReportViewSet

router = DefaultRouter()
router.register(r'reports', ExtensionReportViewSet, basename="Extension report")

urlpatterns = []


urlpatterns += router.urls
