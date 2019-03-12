from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Proposal, Project


# noinspection PyAttributeOutsideInit
class ProjectProposalListTestCase(APITestCase):

    def setUp(self):
        self.project = mommy.make(Project)
        self.employee = mommy.make(User)
        self.url = reverse('project-proposal-list', args=(self.project.pk,))
        self.proposal_data = {'cost': 1000, 'user': self.employee.pk}
        self.expected_data = {
            'project': self.project.title,
            'cost': self.proposal_data['cost'],
            'employer_accepted': False,
            'employee_accepted': False,
            'user': self.proposal_data['user']
        }

    def test_owner_create_proposal_for_employee(self):
        self.client.force_authenticate(user=self.project.owner)
        response = self.client.post(self.url, self.proposal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.expected_data['employer_accepted'] = True
        for key in self.expected_data:
            self.assertEqual(self.expected_data[key], response.data[key])

    def test_employee_create_proposal(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.post(self.url, self.proposal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.expected_data['employee_accepted'] = True
        for key in self.expected_data:
            self.assertEqual(self.expected_data[key], response.data[key])

    def test_unauthorized(self):
        response = self.client.post(self.url, self.proposal_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_denied_on_creating_for_other_users(self):
        self.client.force_authenticate(user=self.employee)
        self.proposal_data['user'] = self.project.owner.pk
        response = self.client.post(self.url, self.proposal_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listing_proposals(self):
        self.client.force_authenticate(user=self.project.owner)
        proposal = mommy.make(Proposal, project=self.project)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['project'], proposal.project.title)

    def test_permission_denied_on_listing_proposals(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# noinspection PyAttributeOutsideInit
class UserProposalListTestCase(APITestCase):

    def setUp(self):
        self.user1 = mommy.make(User)
        self.user2 = mommy.make(User)

        self.proposal = mommy.make(Proposal)
        self.proposal1 = mommy.make(Proposal, project__owner=self.user1, user=self.user2)
        self.proposal2 = mommy.make(Proposal, project__owner=self.user2, user=self.user1)

    def test_proposal_list(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('user-proposal-list', args=(self.user1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_forbidden_proposal_list(self):
        self.client.force_authenticate(user=self.proposal.owner)
        url = reverse('user-proposal-list', args=(self.user1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# noinspection PyAttributeOutsideInit
class ProposalDetailTestCase(APITestCase):

    def setUp(self):
        self.proposal = mommy.make(Proposal)
        self.employee = mommy.make(User)
        self.url = reverse('proposal-detail', args=(self.proposal.pk, ))

    def test_owner_get_proposal(self):
        self.client.force_authenticate(user=self.proposal.project.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cost'], self.proposal.cost)

    def test_employee_get_proposal(self):
        self.client.force_authenticate(user=self.employee)
        self.proposal.user = self.employee
        self.proposal.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forbidden_get_proposal(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# noinspection PyAttributeOutsideInit
class ProposalUpdateTestCase(APITestCase):

    def setUp(self):
        self.proposal = mommy.make(Proposal)
        self.employee = mommy.make(User)
        self.url = reverse('proposal-detail', args=(self.proposal.pk, ))

    def test_forbidden_update_proposal(self):
        self.client.force_authenticate(user=self.proposal.owner)
        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
