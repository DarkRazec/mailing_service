from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, VerificationView, ResetPasswordView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verification_send/', VerificationView.as_view(), name='verification_send'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('password_recovery/', ResetPasswordView.as_view(), name='password_recovery'),
]
