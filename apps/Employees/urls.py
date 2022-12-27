from idlelib.multicall import r

from rest_framework.routers import DefaultRouter
from apps.Employees.views import UsersViewSet, HistoryViewSet, EmployeeViewSet

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'history', HistoryViewSet, basename='stories')
router.register(r'employ', EmployeeViewSet, basename='employs')

urlpatterns = router.urls
