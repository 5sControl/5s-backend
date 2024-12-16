from django.urls import path

from src.Employees.views import CreateUserView, UserListApiView, UserInfoFromToken, UserDetailApiView, \
    WorkplaceEmployees

urlpatterns = [
    path("create/", CreateUserView.as_view()),
    path("", UserListApiView.as_view()),
    path('get-user-info/', UserInfoFromToken.as_view(), name='get-user-info'),
    path('<int:pk>/', UserDetailApiView.as_view(), name='user_detail'),
    path('workplaces/', WorkplaceEmployees.as_view(), name='workplace_employees')
]
