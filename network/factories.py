import factory
from django.utils import timezone

from .models import Post, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("first_name")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    content = factory.Faker("sentence", nb_words=10)
    creation_date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
