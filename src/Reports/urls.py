from rest_framework.routers import DefaultRouter
from django.urls import path, include
from src.Reports.views import ActionsWithPhotos, ReportListView, ActionViewSet


router_report = DefaultRouter()

router_report.register(r"all-reports", ActionViewSet, basename="reports")

urlpatterns = [
    path("report-with-photos/", ActionsWithPhotos.as_view()),
    path("reports/<str:date>/", ReportListView.as_view(), name="machine_action_list"),
    path("", include(router_report.urls)),
]
