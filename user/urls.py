from django.urls import path
from rest_framework.routers import SimpleRouter
from user import views

# router = SimpleRouter()
# router.register(r'user', views.UserList, basename="snippet")

urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path("user/signup", views.sign_up_view),
    path("user/login", views.login_view),
    path("user/logout", views.logout_view),
]
