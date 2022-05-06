from django.urls import path

from network import views

urlpatterns = [
    path("pagenotfound", views.page_not_found, name="pagenotfound"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("index", views.index, name="index"),
    path("", views.PostListView.as_view(), name="post-list"),
    path("following", views.FollowingPostsView.as_view(), name="post-following"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post-detail"),
    path("post/create", views.PostCreateView.as_view(), name="post-create"),
    path("post/update/<int:pk>", views.PostUpdateView.as_view(), name="post-update"),
    path("<slug:username>", views.TimelineView.as_view(), name="user-timeline"),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user-detail"),
]
