from django.urls import path

from .views import (
    GetZlecnieList,
)

urlpatterns = [
    path(
        "zlecenie/",
        GetZlecnieList.as_view(),
        name="get-list-zlecnie",
    ),
]
