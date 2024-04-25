from django.urls import path
from core import views
from django_rest_passwordreset.views import (
    reset_password_request_token,
    reset_password_validate_token,
)
from knox.views import LogoutView


urlpatterns = [
    path("health/", views.HealthCheck.as_view(), name="health"),
    path("health_auth/", views.HealthCheckAuth.as_view(), name="health_auth"),
    path("login/", views.LoginView.as_view(), name="knox_login"),
    path("logout/", LogoutView.as_view(), name="knox_logout"),
    path("me/", views.UserView.as_view(), name="me"),
    path("change_password/", views.ChangePasswordView.as_view()),
    path("password_reset/validate_token/", reset_password_validate_token),
    path("password_reset/confirm/", views.ResetPasswordConfirmView.as_view()),
    path("password_reset/", reset_password_request_token),
]
