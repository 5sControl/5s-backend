from idlelib.multicall import r
from rest_framework.routers import DefaultRouter
from apps.Employees.views import UsersViewSet, HistoryViewSet, EmployeeViewSet, PeopleViewSet
from django.urls import re_path as url
from . import views
from django.conf import settings
from django.conf.urls.static import static



router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'history', HistoryViewSet, basename='stories')
router.register(r'employ', EmployeeViewSet, basename='employs')
router.register(r'count_of_people', PeopleViewSet, basename='people')

urlpatterns = router.urls

urlpatterns += [
    url(r'input/', views.ContactView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
