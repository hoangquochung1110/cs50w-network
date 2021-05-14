class GetSerializerClassMixin(object):
    """
            A class which inhertis this mixins should have variable
            `serializer_action_classes`.
    """

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return self.get_serializer_class()