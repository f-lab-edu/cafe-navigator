from rest_framework.routers import DefaultRouter
from django.urls import path, include
from cafe import views


router = DefaultRouter()
router.register("cafe", views.CafeViewSet)
router.register("cafe/<int:pk>/comment", views.CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
