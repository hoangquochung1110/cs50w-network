import rest_framework_filters as filters
from .models import User, Post

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {'username': ['exact', 'in', 'startswith']}
