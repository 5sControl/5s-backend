from rest_framework.routers import DefaultRouter
from apps.Employees.views import UsersViewSet, LocationUserViewSet

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'location', LocationUserViewSet, basename='location_user')

urlpatterns = router.urls
