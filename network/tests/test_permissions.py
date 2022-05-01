from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from network.factories import PostFactory, UserFactory
from network.permissions import FollowPermission, IsOwner

User = get_user_model()


class IsOwnerTest(TestCase):
    def setUp(self) -> None:
        self.request_user = UserFactory()
        self.target_user = UserFactory()

        self.post_1 = PostFactory(publisher=self.request_user)
        self.post_2 = PostFactory(publisher=self.target_user)

        self.request = Mock()
        self.request.user = self.request_user
        self.view = Mock()
        self.permission = IsOwner()

    def test_is_owner_true(self):
        self.assertTrue(
            self.permission.has_object_permission(
                self.request, self.view, self.post_1
            )
        )

    def test_is_owner_false(self):
        self.assertFalse(
            self.permission.has_object_permission(
                self.request, self.view, self.post_2
            )
        )


class FollowPermissionTest(TestCase):
    def setUp(self) -> None:
        self.request_user = UserFactory()
        self.target_user = UserFactory()

        self.request = Mock()
        self.request.user = self.request_user
        self.view = Mock()
        self.permission = FollowPermission()

    def test_request_user_follow_target_user_success(self):
        self.assertTrue(
            self.permission.has_object_permission(
                self.request, self.view, self.target_user
            )
        )

    def test_request_user_follow_target_user_fail(self):
        self.target_user.followers.add(self.request_user)
        self.assertFalse(
            self.permission.has_object_permission(
                self.request, self.view, self.target_user
            )
        )
