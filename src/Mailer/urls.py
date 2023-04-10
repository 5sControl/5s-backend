from django.urls import path
from src.Mailer.views import SMTPSettingsListCreateView, SMTPSettingsRetrieveUpdateDestroyView, \
    MessagesListCreateAPIView, MessagesDetailAPIView, RecipientsListCreateAPIView, RecipientsDetailAPIView

urlpatterns = [
    path('smtp-settings/', SMTPSettingsListCreateView.as_view(), name='smtp_settings_list_create'),
    path('smtp-settings/<int:pk>/', SMTPSettingsRetrieveUpdateDestroyView.as_view(),
         name='smtp_settings_retrieve_update_destroy'),
    path('messages/', MessagesListCreateAPIView.as_view(), name='messages-list-create'),
    path('messages/int:pk/', MessagesDetailAPIView.as_view(), name='messages-detail'),
    path('recipients/', RecipientsListCreateAPIView.as_view(), name='recipients-list-create'),
    path('recipients/int:pk/', RecipientsDetailAPIView.as_view(), name='recipients-detail'),
]
