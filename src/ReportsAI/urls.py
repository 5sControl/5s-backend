from rest_framework.routers import DefaultRouter
from src.ReportsAI.views import ExtensionReportViewSet

router = DefaultRouter()
router.register(r'reports', ExtensionReportViewSet)

urlpatterns = []


urlpatterns += router.urls
