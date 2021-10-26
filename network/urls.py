
from django.urls import path, include
from rest_framework_nested import routers
from .views import NestedPostViewSet, UserViewSet, PostViewSet, FollowingPostListView,index, register, login_view, logout_view, timeline, following_posts

# router = routers.SimpleRouter()
# router.register('users', UserViewSet)

# users_router = router.NestedSimpleRouter()
# default_router.register('posts', PostViewSet, basename='post-list')

# users_router = routers.NestedSimpleRouter(router, r'users', lookup='publisher')
# users_router.register(r'posts', NestedPostViewSet, basename='user-posts')

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'posts', PostViewSet)
router.register(r'posts/following', FollowingPostListView)

users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', NestedPostViewSet, basename='user-posts')
# 'basename' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

urlpatterns = [

]


urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),
    path("following-post", following_posts, name="following"),
    path("<str:username>", timeline, name="timeline"),

    path(r'', include(router.urls)),
    path(r'', include(users_router.urls)),

]
