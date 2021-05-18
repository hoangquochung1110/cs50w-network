from rest_framework import serializers

from network.models import Post, User


class FollowSerializer(serializers.ModelSerializer):
    """
    Store public information on a specific user
    """
    class Meta:
        model = User
        fields = ['username', 'age', 'gender']


class ReadUserSerializer(serializers.ModelSerializer):
    followers = FollowSerializer(many=True)
    following = FollowSerializer(many=True)
    number_of_following = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'gender', 'followers', 'number_of_followers', 'following', 'number_of_following', ]

    def get_number_of_followers(self, obj):
        return obj.followers.count()

    def get_number_of_following(self, obj):
        return obj.following.count()


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
