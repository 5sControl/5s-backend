from django.urls import path
from .views import DashboardView


urlpatterns = [
    path('<str:date>/', DashboardView.as_view(), name='dashboard_list'),
    # path('name/', DashboardView.as_view(), name='dashboard_list'),
]
