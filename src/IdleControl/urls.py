from rest_framework.routers import DefaultRouter
from django.urls import path, include
from src.IdleControl.views import ActionViewSet, PhotoViewSet


router_machine = DefaultRouter()

router_machine.register(r"action", ActionViewSet, basename="actions")
router_machine.register(r'photos', PhotoViewSet)

urlpatterns = [
    path('action-with-photos/', ActionViewSet.as_view({'get': 'list'}), name='action-with-photos'),
    path('', include(router_machine.urls)),
]
