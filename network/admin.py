from django.contrib import admin

# Register your models here.
from network.models import Post, User

admin.site.register(User)
admin.site.register(Post)
