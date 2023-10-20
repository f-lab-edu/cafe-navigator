from django.urls import path
from rest_framework.routers import SimpleRouter
from user import views

# router = SimpleRouter()
# router.register(r'user', views.UserList, basename="snippet")

urlpatterns = [
    path('user/', views.UserList.as_view(), name="user-list"),
    path('user/<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
    path("user/signup", views.sign_up_view, name="user-signup"),
    path("user/login", views.login_view, name="user-login"),
    path("user/logout", views.logout_view, name="user-logout"),
]
