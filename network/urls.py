
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import PostViewSet

router = routers.DefaultRouter()

router.register('posts', PostViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", include(router.urls))
]
