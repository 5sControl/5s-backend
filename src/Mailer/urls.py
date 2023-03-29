from django.urls import path
from .views import SMTPSettingsListCreateView, SMTPSettingsRetrieveUpdateDestroyView


urlpatterns = [
    path('smtp-settings/', SMTPSettingsListCreateView.as_view(), name='smtp_settings_list_create'),
    path('smtp-settings/<int:pk>/', SMTPSettingsRetrieveUpdateDestroyView.as_view(),
         name='smtp_settings_retrieve_update_destroy'),
]
