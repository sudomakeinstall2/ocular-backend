from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Answer


# noinspection PyAttributeOutsideInit
class AnswerDetailTestCase(APITestCase):

    def setUp(self):
        self.answer = mommy.make(Answer)
        self.url = reverse('answer-detail', args=(self.answer.pk,))
        self.expected_data = {
            'owner': self.answer.owner.id,
            'state': self.answer.state,
            'reason': self.answer.reason,
        }

    def test_get_answer(self):
        self.client.force_authenticate(user=self.answer.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in self.expected_data:
            self.assertEqual(self.expected_data[key], response.data[key])

    def test_anonymous_get_answer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_answer(self):
        self.client.force_authenticate(self.answer.owner)
        payload = {'state': 'accepted'}
        response = self.client.patch(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], payload['state'])

    def test_can_only_update_non_answered(self):
        self.client.force_authenticate(self.answer.owner)
        self.answer.state = Answer.ACCEPTED
        self.answer.save()
        payload = {'state': 'rejected'}
        response = self.client.patch(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
