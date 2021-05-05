from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", related_name='following', symmetrical=False, blank=True)

    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    content = models.TextField(max_length=200)
    publisher = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.content[:5]}... by {self.publisher}'

