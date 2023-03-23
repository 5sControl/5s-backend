from django.urls import path
from .views import CreateSkanyAPIView

urlpatterns = [
    # get data
    path(
        "skany/create/",
        CreateSkanyAPIView.as_view(),
        name="create skany in order",
    ),
]
