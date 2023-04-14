from django.urls import path
from rest_framework.routers import DefaultRouter

from src.Mailer.views import SMTPSettingsListCreateView, SMTPSettingsRetrieveUpdateDestroyView, EmailsView, \
    WorkingTimeView


router = DefaultRouter()
router.register(r"emails", EmailsView, basename="emails")
router.register(r"working-time", WorkingTimeView, basename="working-time")

urlpatterns = [
    path('smtp-settings/', SMTPSettingsListCreateView.as_view(), name='smtp_settings_list_create'),
    path('smtp-settings/<int:pk>/', SMTPSettingsRetrieveUpdateDestroyView.as_view(),
         name='smtp_settings_retrieve_update_destroy')
]

urlpatterns += router.urls
