from rest_framework.routers import DefaultRouter
from django.urls import path, include
from cafe import views


router = DefaultRouter()
router.register("cafe", views.CafeViewSet)
router.register("cafe/search", views.CafeSearchViewSet)
router.register(r"cafe/(?P<cafe_id>\d+)/comment", views.CommentViewSet, basename='comment')
router.register(r"cafe/(?P<cafe_id>\d+)/like", views.LikeViewSet)



urlpatterns = [
    path("", include(router.urls)),
]
