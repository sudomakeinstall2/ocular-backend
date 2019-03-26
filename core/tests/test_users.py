from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase


# noinspection PyAttributeOutsideInit
class ProjectDetailTestCase(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)
        self.url = reverse('self-user-detail')
        self.expected_data = {
            'email': self.user.email,
            'id': self.user.id
        }

    def test_anonymous_get_self(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_self(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in self.expected_data:
            self.assertEqual(self.expected_data[key], response.data[key])
