from rest_framework.routers import DefaultRouter
from django.urls import path
from src.SafetyControl.Safety.views import ActionViewSet, IdleActionListView


router = DefaultRouter()

router.register(r"action", ActionViewSet, basename="Action")

urlpatterns = [
    path('safety_actions/<str:date>/', IdleActionListView.as_view(), name='machine_action_list'),
]

urlpatterns += router.urls
