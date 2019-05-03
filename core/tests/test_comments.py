from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Comment


# noinspection PyAttributeOutsideInit
class CommentListTestCase(APITestCase):

    def setUp(self):
        self.comment = mommy.make(Comment)
        self.url = reverse('comment-list', args=(self.comment.project.id,))
        self.expected_data = {'content': self.comment.content, 'project': self.comment.project.id}

    def test_list_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in self.expected_data:
            self.assertEqual(self.expected_data[key], response.data[0][key])

    def test_create(self):
        self.client.force_authenticate(user=self.comment.owner)
        expected = {
            'content': 'good',
            'owner': self.comment.owner.id,
            'project': self.comment.project.id,
        }
        response = self.client.post(self.url, {'content': 'good'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in expected:
            self.assertEqual(expected[key], response.data[key])

    def test_unauthorized_create(self):
        response = self.client.post(self.url, {'content': 'good'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)