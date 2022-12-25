from rest_framework.routers import DefaultRouter
from apps.Employees.views import UsersViewSet, HistoryViewSet

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'history', HistoryViewSet, basename='stories')

urlpatterns = router.urls
