from django.urls import path

from .views import ActiveResourceView, GetOdooAllItems


urlpatterns = [
    path("status/", ActiveResourceView.as_view(), name="connector-status"),
    path("get_odoo_all_items/", GetOdooAllItems.as_view(), name="get_odoo_all_items")
]
