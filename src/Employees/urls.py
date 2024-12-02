from django.urls import path

from src.Employees.views import CreateUserView, UserListApiView, UserInfoFromToken, UserDetailApiView

urlpatterns = [
    path("create/", CreateUserView.as_view()),
    path("", UserListApiView.as_view()),
    path('get-user-info/', UserInfoFromToken.as_view(), name='get-user-info'),
    path('<int:pk>/', UserDetailApiView.as_view(), name='user_detail'),
]
