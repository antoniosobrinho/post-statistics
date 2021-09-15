from django.db.models import Q, Avg
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from datetime import datetime, timedelta
from pytz import timezone
from post.models import PostLikes
from post.api.serializers import PostLikesSerializer
class PostLikesViewset(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    lookup_field = 'post_id'
    serializer_class = PostLikesSerializer

    def get_queryset(self):

        last_postlikes_entry = PostLikes.objects.filter(
            post_id=self.kwargs['post_id']
        ).order_by('-created_at').first()

        queryset = PostLikes.objects.filter(
            id=last_postlikes_entry.id
        )

        return queryset

class UserStatisticsViewSet(mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):

    lookup_field = 'user_id'
    serializer_class = PostLikesSerializer

    def get_queryset(self):

        queryset = PostLikes.objects.filter(
            user_id=self.kwargs['user_id']
        ).order_by('post_id', '-created_at').distinct('post_id')

        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserAverageLikesView(APIView):

    def get(self, request, user_id, format=None):

        days = 30
        now = datetime.utcnow().replace(
                    tzinfo=timezone(settings.TIME_ZONE)).date()
        thirty_days_before = now - timedelta(days=days)

        try:
            posts_likes =  PostLikes.objects.filter(
                                user_id=int(user_id)
                            ).filter(
                                created_at__gte=thirty_days_before
                            )
            likes_avg = list()
            for i in range(days):
                day = now - timedelta(days=days-i)
                likes_count_avg = posts_likes.filter(
                    Q(created_at__gt=now - timedelta(days=days-i-1)),
                    Q(created_at__lte=now - timedelta(days=days-i))
                ).order_by(
                    'post_id', '-created_at'
                ).distinct('post_id').aggregate(Avg('likes_count'))

                likes_avg.append(
                    {
                        'day': day.strftime("%Y-%m-%d"),
                        'avg': likes_count_avg['avg']
                    }
                )

            return Response(likes_avg)

        except:
            return Response({})

