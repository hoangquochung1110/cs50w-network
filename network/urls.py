
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework import routers as drf_routers
from . import views
from .views import PostViewSet, UserViewSet, PublicPostListView

router = routers.SimpleRouter()
router.register('users', UserViewSet)

default_router = drf_routers.DefaultRouter()
default_router.register('posts', PublicPostListView, basename='post-list')

users_router = routers.NestedSimpleRouter(router, r'users', lookup='publisher')
users_router.register(r'posts', PostViewSet, basename='user-posts')

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>", views.timeline, name="timeline"),
    path("", include(router.urls)),
    path("", include(users_router.urls)),
    path("", include(default_router.urls)),

]
