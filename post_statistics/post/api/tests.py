from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from post.models import PostLikes

class PostTastCase(APITestCase):

    api_client = APIClient()

    def test_post_likes_count(self):

        data = {
            'user_id': 1,
            'post_id': 1,
            'likes_count': 50
        }

        response = self.api_client.post('/api/post/posts/', data,format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_likes_with_another_user(self):

        PostLikes.objects.create(
            user_id=1,
            post_id=1,
            likes_count=10
        )

        data = {
            'user_id': 2,
            'post_id': 1,
            'likes_count': 50
        }

        response = self.api_client.post('/api/post/posts/', data,format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_latest_post_statistics(self):

        PostLikes.objects.create(
            user_id=1,
            post_id=1,
            likes_count=10
        )
        PostLikes.objects.create(
            user_id=1,
            post_id=1,
            likes_count=50
        )

        response = self.api_client.get('/api/post/posts/1/',format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes_count'], 50)

    def test_get_latest_user_post_likes_statistics(self):

        PostLikes.objects.create(
            user_id=1,
            post_id=1,
            likes_count=10
        )
        PostLikes.objects.create(
            user_id=1,
            post_id=1,
            likes_count=50
        )
        PostLikes.objects.create(
            user_id=1,
            post_id=3,
            likes_count=50
        )

        PostLikes.objects.create(
            user_id=2,
            post_id=2,
            likes_count=50
        )

        response_expected = [
            {
                'user_id':1,
                'post_id':1,
                'likes_count':50
            },
            {
                'user_id':1,
                'post_id':3,
                'likes_count':50
            }
        ]
        response = self.api_client.get('/api/post/user-statistics/1/',format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(len(response.data)):
            self.assertEqual(response.data[i]['post_id'], response_expected[i]['post_id'])
            self.assertEqual(response.data[i]['likes_count'], response_expected[i]['likes_count'])
