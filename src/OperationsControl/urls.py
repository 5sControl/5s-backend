from rest_framework.routers import DefaultRouter
from django.urls import path
from src.OperationsControl.views import OperationsControlViewSet, OperationsListView


router_operations = DefaultRouter()

# router_operations.register(r"all_operations", OperationsControlViewSet, basename="all_operations")

urlpatterns = [
    path('all_operations/', OperationsControlViewSet.as_view()),
    path('<str:date>/', OperationsListView.as_view(), name='counter_operations_list'),
]

urlpatterns += router_operations.urls
