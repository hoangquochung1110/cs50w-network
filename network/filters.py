import django_filters

from network.models import Post


class PostFilter(django_filters.FilterSet):
    publisher_username = django_filters.CharFilter(method="publisher_filter")

    class Meta:
        model = Post
        fields = (
            "publisher",
            # "creation_date",
        )

    def publisher_filter(self, queryset, name, value):
        """Filter by publisher's username."""
        return queryset.filter(publisher__username=value)
