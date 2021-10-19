from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets, mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from .mixins import GetSerializerClassMixin
from .models import User, Post
from .serializers import ReadPostSerializer, ReadUserSerializer, WritePostSerializer


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def timeline(request, username):
    user = get_object_or_404(User, username=username)
    print(request.user)
    return render(request, 'network/timeline.html', {'visited_user': user})


class PublicPostListView(mixins.ListModelMixin,
                   GenericViewSet):
    """
    A View for get list of all posts of all users
    """
    queryset = Post.objects.order_by('-published')
    serializer_class = ReadPostSerializer


class PostViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    This view is nested in UserViewSet
    """
    serializer_class = ReadPostSerializer
    permission_classes = [IsAuthenticated,]
    serializer_action_classes = {
        'list': ReadPostSerializer,
        'create': WritePostSerializer,
        'retrieve': ReadPostSerializer,
        'update': WritePostSerializer,
        'destroy': ReadPostSerializer,
    }

    def get_queryset(self):
        queryset = Post.objects.filter(publisher_id=self.kwargs['publisher_pk'])
        if self.action == 'list':
            return queryset.order_by('-published')
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = ReadUserSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            return queryset.filter(id=self.request.user.id)
        return queryset
