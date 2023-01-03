from idlelib.multicall import r
from rest_framework.routers import DefaultRouter
from apps.Employees.views import UsersViewSet, HistoryViewSet, EmployeeViewSet, ContactView
from django.urls import re_path as url
from . import views
# from django.conf.urls import url

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'history', HistoryViewSet, basename='stories')
router.register(r'employ', EmployeeViewSet, basename='employs')
# router.register(r'image', ImageViewSet, basename='images')

urlpatterns = router.urls

urlpatterns += [
    url(r'input/', views.ContactView.as_view()),
]
