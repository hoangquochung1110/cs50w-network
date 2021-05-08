from rest_framework import serializers

from network.models import Post


class ReadPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'publisher', 'published', 'like']


