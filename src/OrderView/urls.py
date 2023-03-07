from django.urls import path
from .views import (
    ZleceniaList,
)

urlpatterns = [
    path('zlecenia/', ZleceniaList.as_view(), name='zlecenia-list'),
]
