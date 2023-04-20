from django.urls import path

from src.Employees.views import CreateUserView, RegisterView, UserListApiView


urlpatterns = [
    path("create/", CreateUserView.as_view()),
    path("register/", RegisterView.as_view()),
    path("", UserListApiView.as_view()),
]
