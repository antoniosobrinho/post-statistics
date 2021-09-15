from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers
from post.api.viewsets import (PostLikesViewset, UserStatisticsViewSet,
                                UserAverageLikesView)

router = routers.SimpleRouter()
router.register(r'posts', PostLikesViewset, basename='posts')
router.register(r'user-statistics', UserStatisticsViewSet, basename='user_statistics')

urlpatterns = [
    url(r'^', include(router.urls)),
    path('user-statistics/<user_id>/average-likes/',
                                UserAverageLikesView.as_view(),name='average-likes')
]
