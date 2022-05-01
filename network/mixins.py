class GetSerializerClassMixin(object):
    """
    A class which inherits this mixins should have variable
    `serializer_action_classes`.
    """

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return self.get_serializer_class()


class GetPermissionClassMixin(object):
    """
    A class which inhertis this mixins should have variable
    `permission_action_classes`.
    """

    def get_permission_class(self):
        print("running mixin")
        try:
            return list(self.permission_action_classes[self.action])
        except (KeyError, AttributeError):
            return self.get_permission_class()


class PermissionsPerMethodMixin(object):
    def get_permissions(self):
        """
        Allows overriding default permissions with @permission_classes
        """
        view = getattr(self, self.action)
        if hasattr(view, "permission_classes"):
            return [permission_class() for permission_class in view.permission_classes]
        return super().get_permissions()
