from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Comment, Like


# noinspection PyAttributeOutsideInit
class LikeListTestCase(APITestCase):

    def setUp(self):
        self.comment = mommy.make(Comment)
        self.url = reverse('like-list', args=(self.comment.id,))

    def test_create(self):
        self.client.force_authenticate(user=self.comment.owner)
        expected = {
            'positive': False,
            'owner': self.comment.owner.email,
            'comment': self.comment.id
        }
        response = self.client.post(self.url, {'positive': 'false'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in expected:
            self.assertEqual(expected[key], response.data[key])

    def test_unauthorized_create(self):
        response = self.client.post(self.url, {'positive': 'false'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LikeDetailTestCase(APITestCase):

    def setUp(self):
        self.like = mommy.make(Like, positive=False)
        self.url = reverse('like-detail', args=(self.like.comment.id, self.like.id))

    def test_unauthorized(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        self.client.force_authenticate(user=self.like.owner)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        self.client.force_authenticate(user=self.like.owner)
        response = self.client.patch(self.url, data={'positive': 'True'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.like.refresh_from_db()
        self.assertEqual(self.like.positive, True)
