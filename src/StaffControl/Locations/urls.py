from rest_framework.routers import DefaultRouter
from src.StaffControl.Locations.views import (
    GateViewSet,
    LocationViewSet,
)

from src.StaffControl.Locations.views import GateViewSet, LocationViewSet

router = DefaultRouter()


router.register(r"gate", GateViewSet, basename="gates")
router.register(r"location", LocationViewSet, basename="locations")


urlpatterns = []
urlpatterns += router.urls
