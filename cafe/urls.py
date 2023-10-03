from rest_framework.routers import SimpleRouter
from django.urls import path, include
from cafe import views


router = SimpleRouter()
router.register('cafe', views.CafeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
