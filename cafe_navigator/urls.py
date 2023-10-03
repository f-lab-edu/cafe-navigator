from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
import user, cafe


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("", include('user.urls')),
    path("", include('cafe.urls')),
]
