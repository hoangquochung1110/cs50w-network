from django.urls import include, path
from rest_framework_nested import routers

from network import views

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet, basename="api-user")
router.register(  # this url pattern should lie at the second highest order
    r"posts/following",
    views.FollowingPostListView,
    basename="post-following",
)
router.register(r"posts", views.PostViewSet, basename="api-post")

users_router = routers.NestedSimpleRouter(router, r"users", lookup="user")
users_router.register(r"posts", views.NestedPostViewSet, basename="user-posts")
# 'basename' is optional. Needed only if the same viewset is registered more than once
# docs on this option: http://www.django-rest-framework.org/api-guide/routers/


urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.PostListView.as_view(), name="post-list"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post-detail"),
    path("post/create", views.PostCreateView.as_view(), name="post-create"),
    path("post/update/<int:pk>", views.PostUpdateView.as_view(), name="post-update"),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user-detail"),
    path("user/follow/<int:pk>", views.FollowView.as_view(), name="user-follow"),
    path("user/unfollow/<int:pk>", views.UnfollowView.as_view(), name="user-unfollow"),
    path("pagenotfound", views.page_not_found, name="pagenotfound"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following-post", views.following_posts, name="following"),
    path("<slug:username>", views.TimelineView.as_view(), name="user-timeline"),
    path(r"", include(router.urls)),
    path(r"", include(users_router.urls)),
]
