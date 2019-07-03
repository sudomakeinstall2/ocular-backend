from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Comment, Project, Like


# noinspection PyAttributeOutsideInit
class CommentListTestCase(APITestCase):

    def setUp(self):
        self.first_project = mommy.make(Project)
        self.second_project = mommy.make(Project)
        self.first_comment = mommy.make(Comment, project=self.first_project)
        self.second_comment = mommy.make(Comment, project=self.second_project)
        self.first_comment.owner.email = 'a@b.com'
        self.url = reverse('comment-list', args=(self.first_comment.project.id,))
        self.expected_data = {
            'content': self.first_comment.content,
            'project': self.first_comment.project.id,
            'id': self.first_comment.id,
        }

    def test_list_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for key in self.expected_data:
            self.assertEqual(self.expected_data[key], response.data[0][key])

    def test_like_count(self):
        mommy.make(Like, comment=self.second_comment, positive=False)
        mommy.make(Like, comment=self.second_comment, positive=False)
        mommy.make(Like, comment=self.second_comment, positive=True)
        url = reverse('comment-list', args=(self.second_comment.project.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['like_count'], -1)

    def test_create(self):
        self.client.force_authenticate(user=self.first_comment.owner)
        expected = {
            'content': 'good',
            'owner': self.first_comment.owner.email,
            'project': self.first_comment.project.id,
        }
        response = self.client.post(self.url, {'content': 'good'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in expected:
            self.assertEqual(expected[key], response.data[key])

    def test_unauthorized_create(self):
        response = self.client.post(self.url, {'content': 'good'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)