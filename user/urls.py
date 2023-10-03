from django.urls import path
from user import views

urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path("user/signup", views.sign_up_view),
    path("user/login", views.login_view),
    path("user/logout", views.logout_view),
]
