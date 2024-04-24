from django.urls import path
from core import views

from knox.views import LogoutView


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="knox_login"),
    path("logout/", LogoutView.as_view(), name="knox_logout"),
    path("me/", views.UserView.as_view(), name="me"),
    path(
        "change_password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
]
