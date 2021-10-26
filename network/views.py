from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets, mixins, status
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from .mixins import GetSerializerClassMixin, GetPermissionClassMixin
from .models import User, Post
from .serializers import ReadPostSerializer, ReadUserSerializer, WritePostSerializer
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .permissions import FollowOthersOnly
import json
from rest_framework.renderers import JSONRenderer


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
    visited_user = get_object_or_404(User, username=username)
    serializer =  ReadUserSerializer(visited_user.followers.all(), many=True)
    return render(request, 'network/timeline.html', {'visited_user': visited_user, 'visited_user_followers': serializer.data})


class PublicPostListView(mixins.ListModelMixin,
                   GenericViewSet):
    """
    A View for get list of all posts of all users
    """
    permission_classes = [AllowAny,]
    queryset = Post.objects.order_by('-published')
    serializer_class = ReadPostSerializer


class PostViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    This view is nested in UserViewSet
    """
    queryset = Post.objects.all()
    serializer_class = ReadPostSerializer
    permission_classes = [IsAuthenticated,]
    serializer_action_classes = {
        'list': ReadPostSerializer,
        'create': WritePostSerializer,
        'retrieve': ReadPostSerializer,
        'partial_update': WritePostSerializer,
        'update': WritePostSerializer,
        'destroy': ReadPostSerializer,
    }

    def get_queryset(self):
        publisher_id = self.kwargs['user_pk']
        queryset = Post.objects.filter(publisher_id=publisher_id)
        if self.action == 'list':
            return queryset.order_by('-published')
        return queryset


class UserViewSet(GetSerializerClassMixin,viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    serializer_action_classes = {
        'list': ReadUserSerializer,
        'create': ReadUserSerializer,
        'retrieve': ReadUserSerializer,
        'partial_update': ReadUserSerializer,
        'update': ReadUserSerializer,
        'destroy': ReadUserSerializer,
        'follow': None,
        'unfollow': None,
    }

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            return queryset.filter(id=self.request.user.id)
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[FollowOthersOnly,])
    def follow(self, request, pk):
        visited_user = self.get_object()
        visited_user.followers.add(request.user)
        response_serializer = ReadUserSerializer(instance=request.user)
        return Response(response_serializer.data)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk):
        visited_user = self.get_object()
        request.user.following.remove(visited_user)
        request.user.save()
        response_serializer = ReadUserSerializer(instance=request.user)
        return Response(response_serializer.data)

