from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Project


# noinspection PyAttributeOutsideInit
class ProposalTestCase(APITestCase):

    def setUp(self):
        self.project = mommy.make(Project)
        self.employee = mommy.make(User)
        self.url = reverse('project-detail', args=(self.project.pk,))
        self.expected_data = {
            'owner': self.project.owner.email,
            'title': self.project.title,
            'description': self.project.description,
            'deadline': str(self.project.deadline),
            'cost': self.project.cost
        }

    def test_anonymous_get_project(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in self.expected_data:
            self.assertEqual(self.expected_data[key], response.data[key])

    def test_update_project(self):
        self.client.force_authenticate(user=self.project.owner)
        payload = {'title': 'new'}
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], payload['title'])

    def test_forbidden_update_project(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
