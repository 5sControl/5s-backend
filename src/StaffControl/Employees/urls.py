from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, PeopleViewSet, UsersViewSet, CreateUserView

router = DefaultRouter()

# router.register(r"admin", UsersViewSet, basename="users")
# router.register(r"employ", EmployeeViewSet, basename="employs")
# router.register(r"count-of-people", PeopleViewSet, basename="all people in locations")

urlpatterns = [
    # path("create/user/", CreateUserView.as_view(), name="create admin/worker"),
]


urlpatterns += router.urls
