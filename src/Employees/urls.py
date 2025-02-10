from django.urls import path

from src.Employees.views import CreateUserView, UserListApiView, UserInfoFromToken, UserDetailApiView, \
    WorkplaceEmployees, VerifyResetCodeView, SetNewPasswordView, SendPasswordResetCodeView

urlpatterns = [
    path("create/", CreateUserView.as_view()),
    path("", UserListApiView.as_view()),
    path('get-user-info/', UserInfoFromToken.as_view(), name='get-user-info'),
    path('<int:pk>/', UserDetailApiView.as_view(), name='user_detail'),
    path('workplaces/', WorkplaceEmployees.as_view(), name='workplace_employees'),
    path('password-reset/', SendPasswordResetCodeView.as_view(), name='send_reset_code'),
    path('verify-reset-code/', VerifyResetCodeView.as_view(), name='verify_reset_code'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
]
