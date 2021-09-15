from django.db import models
# Create your models here.
class PostLikes(models.Model):

    user_id = models.PositiveIntegerField()
    post_id = models.PositiveIntegerField()
    likes_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




