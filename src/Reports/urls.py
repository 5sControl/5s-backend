from rest_framework.routers import DefaultRouter
from django.urls import path, include
from src.Reports.views import ActionsWithPhotos, IdleActionListView, ActionViewSet


router_report = DefaultRouter()

router_report.register(r"all_reports", ActionViewSet, basename="reports")

urlpatterns = [
    path('report-with-photos/', ActionsWithPhotos.as_view()),
    path('report_actions/<str:date>/', IdleActionListView.as_view(), name='machine_action_list'),
    path('', include(router_report.urls)),
]
