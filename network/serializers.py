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
    # posts = ReadPostSerializer(many=True)
    number_of_following = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()
    number_of_posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'age',
            'gender',
            'followers',
            'number_of_followers',
            'following',
            'number_of_following',
            'number_of_posts',
        ]


    def get_number_of_followers(self, obj):
        return obj.followers.count()

    def get_number_of_following(self, obj):
        return obj.following.count()

    def get_number_of_posts(self, obj):
        return obj.posts.count()


class ReadPostSerializer(serializers.ModelSerializer):
    publisher = ReadUserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'content', 'publisher', 'published', 'like']


class WritePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content', ]

    def create(self, validated_data):
        publisher = User.objects.get(pk=self.context["view"].kwargs["publisher_pk"])
        validated_data["publisher"] = publisher
        return Post.objects.create(**validated_data)
