from rest_framework.permissions import BasePermission


class FollowPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user != obj and not(request.user.following.filter(id=obj.id).exists()):
            return True
        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.posts.filter(id=obj.id)