from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.references.views import ConnectionErpReferenceView

router = DefaultRouter()

urlpatterns = [
    path('products/', ConnectionErpReferenceView.as_view(), name='products'),
    path("", include(router.urls)),
]
