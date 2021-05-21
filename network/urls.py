
from django.urls import path, include
from rest_framework_nested import routers
from . import views
from .views import PostViewSet, UserViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet)

users_router = routers.NestedSimpleRouter(router, r'users', lookup='publisher')
users_router.register(r'posts', PostViewSet, basename='user-posts')

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", include(router.urls)),
    path("", include(users_router.urls)),

]
