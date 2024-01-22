from rest_framework.routers import DefaultRouter
from .views import SocialPostViewSet

router = DefaultRouter()
router.register(r'reports', SocialPostViewSet)

urlpatterns = []


urlpatterns += router.urls
