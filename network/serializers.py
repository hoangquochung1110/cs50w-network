from rest_framework import serializers

from network.models import Post, User


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'gender',]


class ReadPostSerializer(serializers.ModelSerializer):
    publisher = ReadUserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'content', 'publisher', 'published', 'like']


class WritePostSerializer(serializers.ModelSerializer):
    publisher = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['content', 'publisher', ]
