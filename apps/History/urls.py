from rest_framework.routers import DefaultRouter

from .views import HistoryViewSet

router = DefaultRouter()

router.register(r'', HistoryViewSet, basename='History records')
# router.register(r'record', , basename='people')

urlpatterns = router.urls
