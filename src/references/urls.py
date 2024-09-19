from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.references.views import ErpReferenceProductsView, ReferenceOperationsView, ReferenceEquipmentView, ReferenceEmployeesView

router = DefaultRouter()

urlpatterns = [
    path('products/', ErpReferenceProductsView.as_view(), name='products'),
    path('operations/', ReferenceOperationsView.as_view(), name='operations'),
    path('employees/', ReferenceEmployeesView.as_view(), name='employees'),
    path('equipment/', ReferenceEquipmentView.as_view(), name='equipment'),
    path("", include(router.urls)),
]
