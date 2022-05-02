from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from network.filters import PostFilter
from network.forms import PostCreateForm

from .models import Post, User


def index(request):
    if request.user.is_anonymous:
        request.session["user_id"] = -1
    return render(request, "index.html")


def page_not_found(request):
    return render(request, "notfound.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("post-list"))
        else:
            return render(
                request,
                "login.html",
                {"message": "Invalid username and/or password."},
            )
    else:

        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("post-list"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "register.html")


class PostListView(ListView):
    """View displays list of posts."""

    model = Post
    template_name = "post/list.html"
    queryset = Post.objects.all().order_by("-creation_date")
    filter_model = PostFilter

    def get_queryset(self):
        filterset_model = self.filter_model(
            request=self.request, queryset=self.queryset
        )
        return filterset_model

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        filter_model = self.filter_model(
            request=self.request,
            queryset=self.queryset,
        )
        context_data["filter"] = filter_model
        return context_data


class PostDetailView(DetailView):
    """View for a specific post."""

    model = Post
    template_name = "fragments/post/detail.html"


class PostCreateView(CreateView):
    """View for post creation."""

    model = Post
    form_class = PostCreateForm
    template_name = "fragments/post/create.html"
    success_url = reverse_lazy("post-list")

    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.publisher = self.request.user
            post.save()
            return render(request, "fragments/post/detail.html", {"object": post})
        return HttpResponseRedirect(reverse("post-list"))


class PostUpdateView(UpdateView):
    """View for post update."""

    model = Post
    form_class = PostCreateForm
    template_name = "fragments/post/update.html"

    def form_valid(self, form):
        """Insert HX-Redirect attribute to response header.

        The purpose is to modify htmx swapping mechanism
        in case of successful update.
        """
        form.save()
        return HttpResponseRedirect(reverse("post-detail", args=[self.object.id]))


class UserDetailView(DetailView):
    """View for publisher detail."""

    model = User
    template_name = "fragments/user/detail.html"


class TimelineView(DetailView):
    """View for a specific publisher."""

    model = User
    template_name = "user/timeline.html"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        username = self.kwargs["username"]
        return User.objects.get(username=username)


class FollowingPostsView(ListView):
    """View for list of posts an user is following."""

    model = Post
    template_name = "post/list.html"

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(
            publisher__in=following_users
        ).order_by("-creation_date")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # to sync with PostListView, avoid KeyError in list.html
        context_data["filter"] = {"qs": context_data["object_list"]}
        return context_data
