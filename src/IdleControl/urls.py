from rest_framework.routers import DefaultRouter
from django.urls import path, include
from src.IdleControl.views import ActionViewSet, ActionsWithPhotos, IdleActionListView


router_idle = DefaultRouter()

router_idle.register(r"action", ActionViewSet, basename="actions")

urlpatterns = [
    path('action-with-photos/', ActionsWithPhotos.as_view()),
    path('idle_actions/<str:date>/', IdleActionListView.as_view(), name='machine_action_list'),
    path('', include(router_idle.urls)),
]
