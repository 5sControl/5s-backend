from rest_framework.routers import DefaultRouter
from apps.Locations.views import CameraViewSet, GateViewSet, LocationViewSet

router = DefaultRouter()

router.register(r'camera', CameraViewSet, basename='cameras')
router.register(r'gate', GateViewSet, basename='gates')
router.register(r'location', LocationViewSet, basename='locations')

urlpatterns = router.urls
