from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path

from src.Employees.views import CreateUserView, UserListApiView, UserInfoFromToken, UserDetailApiView, \
    WorkplaceEmployees, PasswordResetRequestView, PasswordResetCompleteView

urlpatterns = [
    path("create/", CreateUserView.as_view()),
    path("", UserListApiView.as_view()),
    path('get-user-info/', UserInfoFromToken.as_view(), name='get-user-info'),
    path('<int:pk>/', UserDetailApiView.as_view(), name='user_detail'),
    path('workplaces/', WorkplaceEmployees.as_view(), name='workplace_employees'),
    path("password-reset/", PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
