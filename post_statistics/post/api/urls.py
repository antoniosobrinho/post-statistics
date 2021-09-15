from django.conf.urls import include, url
from rest_framework import routers
from post.api.viewsets import PostLikesViewset

router = routers.SimpleRouter()
router.register(r'posts', PostLikesViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
]
