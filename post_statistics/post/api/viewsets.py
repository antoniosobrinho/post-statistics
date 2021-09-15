from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, mixins
from post.models import PostLikes
from post.api.serializers import PostLikesSerializer

class PostLikesViewset(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    queryset = PostLikes.objects.all()
    serializer_class = PostLikesSerializer
