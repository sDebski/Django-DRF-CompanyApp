from django.urls import path
from core import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="knox_login"),
    path("me/", views.UserView.as_view(), name="me"),
]
