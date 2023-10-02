from django.urls import path
from user import views

urlpatterns = [
    path("signup", views.sign_up),
    path("login", views.login_view),
    path("logout", views.logout_view),
]
