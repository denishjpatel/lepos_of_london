from django.urls import path
from . import views

urlpatterns = [
    path("login", views.loginview, name="loginview"),
    path("logout", views.logoutview, name="logoutview"),
    path("register", views.register, name="register"),
    path("send_link", views.send_link, name="send_link"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("change_password", views.change_password, name="change_password"),
    path("update_profile", views.update_profile, name="update_profile"),
    
]