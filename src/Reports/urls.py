from rest_framework.routers import DefaultRouter
from django.urls import path, include
from src.Reports.views import (
    ActionsWithPhotos,
    ReportListView,
    ActionViewSet,
    SearchReportListView,
    GetOperationVideoInfo,
)


router_report = DefaultRouter()

router_report.register(r"all_reports", ActionViewSet, basename="reports")

urlpatterns = [
    path("report-with-photos/", ActionsWithPhotos.as_view()),
    path(
        "search/<str:algorithm_name>/<str:camera_ip>/<str:date>/<str:start_time>/<str:end_time>/",
        ReportListView.as_view(),
        name="report_action_list",
    ),
    path("search_params/", SearchReportListView.as_view()),
    path("video-info/", GetOperationVideoInfo.as_view()),
    path("", include(router_report.urls)),
]
