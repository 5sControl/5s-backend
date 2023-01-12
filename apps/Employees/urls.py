from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, HistoryViewSet, PeopleViewSet, UsersViewSet

router = DefaultRouter()

router.register(r'admin', UsersViewSet, basename='users')
router.register(r'history', HistoryViewSet, basename='stories')
router.register(r'employ', EmployeeViewSet, basename='employs')
router.register(r'count_of_people', PeopleViewSet, basename='people')

urlpatterns = router.urls
