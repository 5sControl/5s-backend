from rest_framework.routers import DefaultRouter
from apps.Employees.views import UsersViewSet, HistoryViewSet, EmployeeViewSet, PeopleViewSet


router = DefaultRouter()

router.register(r'admins', UsersViewSet, basename='users')
router.register(r'history', HistoryViewSet, basename='stories')
router.register(r'employ', EmployeeViewSet, basename='employs')
router.register(r'count_of_people', PeopleViewSet, basename='people')

urlpatterns = router.urls