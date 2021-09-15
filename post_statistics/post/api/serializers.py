from rest_framework import serializers
from post.models import PostLikes

class PostLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLikes
        exclude = ['created_at', 'updated_at']

