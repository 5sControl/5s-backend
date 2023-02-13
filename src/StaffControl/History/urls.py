from .views import HistoryViewSet, FilteredHistoryModelViewSet

from django.urls import path

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"all_record", HistoryViewSet, basename="all History")
urlpatterns = router.urls

urlpatterns += [
    path(
        "filtered_records/",
        FilteredHistoryModelViewSet.as_view(),
        name="History records",
    )
]
