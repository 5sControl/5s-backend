from django.urls import path

from src.Employees.views import CreateUserView, UserListApiView


urlpatterns = [
    path("create/", CreateUserView.as_view()),
    path("", UserListApiView.as_view()),
]
