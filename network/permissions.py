from rest_framework.permissions import BasePermission


class FollowOthersOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user != obj


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.posts.filter(id=obj.id)