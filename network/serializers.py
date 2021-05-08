from rest_framework import serializers

from network.models import Post, User


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ReadPostSerializer(serializers.ModelSerializer):
    publisher = ReadUserSerializer()

    class Meta:
        model = Post
        fields = ['content', 'publisher', 'published', 'like']


