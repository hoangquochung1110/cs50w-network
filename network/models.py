from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    NOT_GIVEN = 'NG'

    GENDER_CHOICES = [
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
        (NOT_GIVEN, 'NOT_GIVEN')
    ]

    followers = models.ManyToManyField("self", related_name='following', symmetrical=False, blank=True)
    age = models.SmallIntegerField(help_text="How old are you ?", default=0)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=NOT_GIVEN)

    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    content = models.TextField(max_length=200)
    publisher = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.content[:5]}... by {self.publisher}'

