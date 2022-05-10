from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from network.api.serializers import (ReadPostSerializer, ReadUserSerializer,
                                     WritePostSerializer)
from network.models import Post, User

from ..mixins import GetSerializerClassMixin
from ..permissions import FollowPermission, IsOwner


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
            return render(request, "fragments/post/detail.html", {"pk": post_obj.id})
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
            return render(request, "fragments/post/detail.html", {"pk": post_obj.id})
        return Response(
            {
                "detail": "user %s can not unlike the post without liking it first"
                % request.user
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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
        return render(
            request,
            "fragments/user/follow.html",
            {"object": visited_user},
        )

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk):
        visited_user = self.get_object()
        request.user.following.remove(visited_user)
        request.user.save()
        return render(
            request,
            "fragments/user/follow.html",
            {"object": visited_user},
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
