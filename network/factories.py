import factory
from .models import User, Post
from django.utils import timezone

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('first_name')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    
    content = factory.Faker('sentence', nb_words=10)
    creation_date = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
