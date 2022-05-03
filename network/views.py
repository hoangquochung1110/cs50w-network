from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from jsonschema import ValidationError
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from network.filters import PostFilter
from network.forms import PostCreateForm

from .mixins import GetSerializerClassMixin
from .models import Post, User
from .permissions import FollowPermission, IsOwner
from .serializers import (ReadPostSerializer, ReadUserSerializer,
                          WritePostSerializer)


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
            request.session["user_id"] = user.id
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:

        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
                "network/register.html",
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


def timeline(request, username):
    visited_user = get_object_or_404(User, username=username)
    serializer = ReadUserSerializer(visited_user.followers.all(), many=True)
    return render(
        request,
        "user/timeline.html",
        context={
            "visited_user": visited_user,
            "visited_user_followers": serializer.data,
        },
    )


def following_posts(request):
    return render(request, "index.html", context={"following_posts": True})


class PostViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Post.objects.order_by("-creation_date")
    serializer_action_classes = {
        "list": ReadPostSerializer,
        "create": WritePostSerializer,
        "retrieve": ReadPostSerializer,
        "partial_update": WritePostSerializer,
        "update": WritePostSerializer,
        "destroy": ReadPostSerializer,
        "like": None,
        "unlike": None,
    }

    def get_permissions(self):
        if self.action == "update" or self.action == "partial_update":
            permission_classes = [
                IsOwner,
            ]
        elif self.action == "list":
            permission_classes = [
                AllowAny,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def like(self, request, pk):
        post_obj = Post.objects.get(pk=pk)
        liked = post_obj.liked_by.filter(id=request.user.id).exists()
        if not liked:
            post_obj.like += 1
            post_obj.liked_by.add(request.user)
            post_obj.save()
            response_serializer = ReadPostSerializer(instance=post_obj)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "user %s can not like the post more than once" % request.user},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @action(detail=True, methods=["post"])
    def unlike(self, request, pk):
        post_obj = Post.objects.get(pk=pk)
        liked = post_obj.liked_by.filter(id=request.user.id).exists()
        if liked:
            post_obj.like -= 1
            post_obj.liked_by.remove(request.user)
            post_obj.save()
            response_serializer = ReadPostSerializer(instance=post_obj)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {
                "detail": "user %s can not unlike the post without liking it first"
                % request.user
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class FollowingPostListView(mixins.ListModelMixin, GenericViewSet):
    """
    A View for getting list of posts which a given user is following
    """

    queryset = Post.objects.none()
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ReadPostSerializer

    def get_queryset(self):
        return Post.objects.filter(publisher__followers=self.request.user).order_by(
            "-creation_date"
        )


class NestedPostViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    This view is nested in UserViewSet
    """

    queryset = Post.objects.all()
    serializer_class = ReadPostSerializer
    permission_classes = [
        AllowAny,
    ]
    serializer_action_classes = {
        "list": ReadPostSerializer,
        "create": WritePostSerializer,
        "retrieve": ReadPostSerializer,
        "partial_update": WritePostSerializer,
        "update": WritePostSerializer,
        "destroy": ReadPostSerializer,
    }

    def get_queryset(self):
        publisher_id = self.kwargs["user_pk"]
        queryset = Post.objects.filter(publisher_id=publisher_id)
        if self.action == "list":
            return queryset.order_by("-creation_date")
        return queryset


class UserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = None

    serializer_action_classes = {
        "list": ReadUserSerializer,
        "create": ReadUserSerializer,
        "retrieve": ReadUserSerializer,
        "partial_update": ReadUserSerializer,
        "update": ReadUserSerializer,
        "destroy": ReadUserSerializer,
        "follow": None,
        "unfollow": None,
    }

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [
                AllowAny,
            ]
        elif self.action == "follow":
            permission_classes = [
                FollowPermission,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.filter(id=self.request.user.id)
        return queryset

    @action(detail=True, methods=["post"])
    def follow(self, request, pk):
        visited_user = self.get_object()
        visited_user.followers.add(request.user)
        response_serializer = ReadUserSerializer(instance=visited_user)
        return Response(response_serializer.data)

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk):
        visited_user = self.get_object()
        request.user.following.remove(visited_user)
        request.user.save()
        response_serializer = ReadUserSerializer(instance=visited_user)
        return Response(response_serializer.data)


class PostListView(ListView):
    """View displays list of posts."""

    model = Post
    template_name = "post/list.html"
    ordering = ("creation_date",)
    filter_model = PostFilter

    def get_queryset(self):
        qs = Post.objects.select_related("publisher").all()
        filterset_model = self.filter_model(request=self.request, queryset=qs)
        return filterset_model.qs.order_by(*self.ordering)

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


class FollowView(UpdateView):
    """View to follow/un-follow a specific user."""

    def post(self, request, *args, **kwargs):
        instance_id = kwargs["pk"]
        instance = User.objects.get(id=instance_id)
        followers_qs = instance.followers.all()
        if self.request.user not in followers_qs:
            instance.followers.add(self.request.user)
            instance.save()
            return render(
                request,
                "fragments/user/follow.html",
                {"object": instance},
            )
        raise ValidationError("Can not follow user that you are following")


class UnfollowView(UpdateView):
    """View to unfollow a specific user."""

    def post(self, request, *args, **kwargs):
        instance_id = kwargs["pk"]
        instance = User.objects.get(id=instance_id)
        followers_qs = instance.followers.all()
        if self.request.user in followers_qs:
            instance.followers.remove(self.request.user)
            instance.save()
            return render(
                request,
                "fragments/user/follow.html",
                {"object": instance}
            )
        raise ValidationError("Can not unfollow user that you are not following")
