from idlelib.multicall import r
from rest_framework.routers import DefaultRouter
from apps.Employees.views import UsersViewSet, HistoryViewSet, EmployeeViewSet, ContactView, PeopleViewSet
from django.urls import re_path as url
from . import views

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'history', HistoryViewSet, basename='stories')
router.register(r'employ', EmployeeViewSet, basename='employs')
router.register(r'people', PeopleViewSet, basename='people')

urlpatterns = router.urls

urlpatterns += [
    url(r'input/', views.ContactView.as_view()),
]
