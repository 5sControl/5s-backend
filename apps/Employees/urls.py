from rest_framework.routers import DefaultRouter
from apps.Employees.views import UsersViewSet

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = router.urls
