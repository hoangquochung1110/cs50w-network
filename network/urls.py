from django.urls import include, path
from rest_framework_nested import routers

from network import views

# router = routers.SimpleRouter()
# router.register('users', UserViewSet)

# users_router = router.NestedSimpleRouter()
# default_router.register('posts', PostViewSet, basename='post-list')

# users_router = routers.NestedSimpleRouter(router, r'users', lookup='publisher')
# users_router.register(r'posts', NestedPostViewSet, basename='user-posts')

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet, basename="users")
router.register(
    r"posts/following", views.FollowingPostListView
)  # this url pattern should lie at the second highest order
router.register(r"posts", views.PostViewSet)

users_router = routers.NestedSimpleRouter(router, r"users", lookup="user")
users_router.register(r"posts", views.NestedPostViewSet, basename="user-posts")
# 'basename' is optional. Needed only if the same viewset is registered more than once
# docs on this option: http://www.django-rest-framework.org/api-guide/routers/

urlpatterns = []


urlpatterns = [
    path("", views.index, name="index"),
    path("pagenotfound", views.page_not_found, name="pagenotfound"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following-post", views.following_posts, name="following"),
    path("<str:username>", views.timeline, name="timeline"),
    path(r"", include(router.urls)),
    path(r"", include(users_router.urls)),
]
