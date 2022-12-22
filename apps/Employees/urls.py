from rest_framework.routers import DefaultRouter
from apps.Employees.views import MessageProfileViewSet, ProfileViewSet

router = DefaultRouter()

router.register(r'message', MessageProfileViewSet, basename='message_profiles')
router.register(r'profile', ProfileViewSet, basename='profiles')

urlpatterns = router.urls