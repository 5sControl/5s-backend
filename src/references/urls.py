from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.references.views import ErpReferenceView

router = DefaultRouter()

urlpatterns = [
    path('erp-reference/<str:reference_type>/', ErpReferenceView.as_view(), name='erp-reference'),
    path("", include(router.urls)),
]
