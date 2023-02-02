from rest_framework.routers import DefaultRouter
from apps.Safety.views import ActionViewSet


router = DefaultRouter()

router.register(r'action', ActionViewSet, basename='Action')

urlpatterns = router.urls
