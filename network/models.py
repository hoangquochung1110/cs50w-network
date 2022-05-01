from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NOT_GIVEN = "NOT GIVEN"

    GENDER_CHOICES = [
        (MALE, "MALE"),
        (FEMALE, "FEMALE"),
        (NOT_GIVEN, "NOT_GIVEN"),
    ]

    followers = models.ManyToManyField(
        "self", related_name="following", symmetrical=False, blank=True
    )
    age = models.SmallIntegerField(help_text="How old are you ?", default=0)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default=NOT_GIVEN
    )

    def __str__(self):
        return f"{self.username}"

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def posts_count(self):
        return self.posts.count()


class Post(models.Model):
    content = models.TextField(max_length=200)
    publisher = models.ForeignKey(
        User, related_name="posts", on_delete=models.SET_NULL, null=True
    )  # TODO: should be posts (plural) or post (singular)
    creation_date = models.DateTimeField()
    last_modified = models.DateTimeField(null=True, blank=True)
    like = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="likers", blank=True)

    def __str__(self):
        return f"{self.content[:5]}... by {self.publisher}"

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()

        self.last_modified = timezone.now()
        return super(Post, self).save(*args, **kwargs)
