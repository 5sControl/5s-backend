from rest_framework.routers import DefaultRouter

from .views import HistoryViewSet

from django.urls import path

router = DefaultRouter()

router.register(r'', HistoryViewSet, basename='History records')

urlpatterns = router.urls

