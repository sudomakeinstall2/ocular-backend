from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Milestone, Project


# noinspection PyAttributeOutsideInit
class MilestoneDetail(APITestCase):

    def setUp(self):
        self.milestone = mommy.make(Milestone)
        self.employee = mommy.make(User)
        self.url = reverse('milestone-detail', args=(self.milestone.project.pk, self.milestone.pk))

    def test_get_milestone(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_milestone(self):
        self.client.force_authenticate(self.milestone.project.owner)
        payload = {'title': 'new'}
        response = self.client.patch(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], payload['title'])

    def test_forbidden_update_milestone(self):
        self.client.force_authenticate(self.employee)
        response = self.client.patch(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MilestoneList(APITestCase):

    def setUp(self):
        self.project = mommy.make(Project, deadline='2020-01-01')
        self.url = reverse('milestone-list', args=(self.project.pk, ))

    def test_invalid_create_milestone_after_deadline(self):
        self.client.force_authenticate(self.project.owner)
        payload = {
            'title': 'hi',
            'description': 'extra',
            'deadline': '2020-01-02',
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
