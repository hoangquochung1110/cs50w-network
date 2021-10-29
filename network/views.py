import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets, mixins, status
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from .mixins import GetSerializerClassMixin, GetPermissionClassMixin
from .models import User, Post
from .serializers import ReadPostSerializer, ReadUserSerializer, WritePostSerializer
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .permissions import FollowOthersOnly
from rest_framework.renderers import JSONRenderer
from .permissions import IsOwner

def index(request):
    if request.user.is_anonymous:
        request.session['user_id'] = -1
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
            request.session['user_id'] = user.id
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
    return render(request, 'network/timeline.html', context={'visited_user': visited_user, 'visited_user_followers': serializer.data})


def following_posts(request):
    return render(request, 'network/index.html', context={'following_posts': True})


class PostViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Post.objects.order_by('-creation_date')
    serializer_action_classes = {
        'list': ReadPostSerializer,
        'create': WritePostSerializer,
        'retrieve': ReadPostSerializer,
        'partial_update': WritePostSerializer,
        'update': WritePostSerializer,
        'destroy': ReadPostSerializer,
        'like': None,
        'unlike': None,
    }

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwner, ]
        elif self.action == 'list':
            permission_classes = [AllowAny,]
        else:
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def like(self, request, pk):
        post_obj = Post.objects.get(pk=pk)
        liked = post_obj.liked_by.filter(id=request.user.id).exists()
        if not liked:
            post_obj.like += 1
            post_obj.liked_by.add(request.user)
            post_obj.save()
            response_serializer = ReadPostSerializer(instance=post_obj)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'user %s can not like the post more than once' % request.user}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['post'])
    def unlike(self, request, pk):
        post_obj = Post.objects.get(pk=pk)
        liked = post_obj.liked_by.filter(id=request.user.id).exists()
        if liked:
            post_obj.like -= 1
            post_obj.liked_by.remove(request.user)
            post_obj.save()
            response_serializer = ReadPostSerializer(instance=post_obj)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'user %s can not unlike the post without liking it first' % request.user}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowingPostListView(mixins.ListModelMixin, GenericViewSet):
    """
    A View for getting list of posts which a given user is following
    """
    queryset = Post.objects.none()
    permission_classes = [IsAuthenticated,]
    serializer_class = ReadPostSerializer

    def get_queryset(self):
        return Post.objects.filter(publisher__followers=self.request.user).order_by('-creation_date')


class NestedPostViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    This view is nested in UserViewSet
    """
    queryset = Post.objects.all()
    serializer_class = ReadPostSerializer
    permission_classes = [AllowAny,]
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
            return queryset.order_by('-creation_date')
        return queryset


class UserViewSet(GetSerializerClassMixin,viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = None

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

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

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

