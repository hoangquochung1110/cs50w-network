from django.urls import include, path
from rest_framework_nested import routers

from network.api import views

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet, basename="api-user")
router.register(r"posts", views.PostViewSet, basename="api-post")

users_router = routers.NestedSimpleRouter(router, r"users", lookup="user")
users_router.register(r"posts", views.NestedPostViewSet, basename="user-posts")
# 'basename' is optional. Needed only if the same viewset is registered more than once
# docs on this option: http://www.django-rest-framework.org/api-guide/routers/

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(users_router.urls)),
]
