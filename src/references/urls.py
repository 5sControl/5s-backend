from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import re_path

from src.references.views import ErpReferenceView

router = DefaultRouter()

urlpatterns = [
    re_path(r'^(?P<reference_type>.*)/$', ErpReferenceView.as_view(), name='erp-reference'),
    path("", include(router.urls)),
]
