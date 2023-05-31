from django.urls import path

from .views import (
    GetOperationData,
)

urlpatterns = [
    path(
        "operations/",
        GetOperationData.as_view(),
        name="get-list-zlecnie",
    ),
]
