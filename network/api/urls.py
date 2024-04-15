from django.urls import include, path
from rest_framework.routers import DefaultRouter

from network.api import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="api-user")
router.register(r"posts", views.PostViewSet, basename="api-post")

# 'basename' is optional. Needed only if the same viewset is registered more than once
# docs on this option: http://www.django-rest-framework.org/api-guide/routers/

urlpatterns = [
    path(r"", include(router.urls)),
]
