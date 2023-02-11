from rest_framework.routers import DefaultRouter
from src.SafetyControl.Safety.views import ActionViewSet


router = DefaultRouter()

router.register(r"action", ActionViewSet, basename="Action")

urlpatterns = router.urls
