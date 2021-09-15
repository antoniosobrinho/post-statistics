from django.db.models import Q
from rest_framework import serializers
from post.models import PostLikes

class PostLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLikes
        exclude = ['id']

    def validate(self, attrs):
        super().validate(attrs)
        posts = PostLikes.objects.filter(
            Q(post_id=attrs['post_id']),
            ~Q(user_id=attrs['user_id'])
        )
        if posts.exists():
            raise serializers.ValidationError(
                                    "The post already saved with another user.")

        return attrs


