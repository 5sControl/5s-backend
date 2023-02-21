from rest_framework.routers import DefaultRouter
from django.urls import path, include
from src.Reports.views import ActionsWithPhotos, ReportListView, ActionViewSet, ReportListAPIView


router_report = DefaultRouter()

router_report.register(r"all_reports", ActionViewSet, basename="reports")

urlpatterns = [
    path("report-with-photos/", ActionsWithPhotos.as_view()),
    path("reports/<str:date>/", ReportListView.as_view(), name="machine_action_list"),
    path('reports/<str:start_date>/<str:end_date>/', ReportListAPIView.as_view(), name='report_list_api'),
    path("", include(router_report.urls)),
]
