import logging

from rest_framework import generics, permissions

from core.permissions import IsProjectOwner, IsReadOnly, IsEmployeeCreatingProposalForHerself
from .models import Milestone, Project, Proposal
from .serializers import (MilestoneSerializer, ProjectSerializer,
                          ProposalSerializer)

logger = logging.getLogger(__name__)


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MilestoneList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated | IsReadOnly, IsReadOnly | IsProjectOwner,)
    serializer_class = MilestoneSerializer

    def get_queryset(self):
        return Milestone.objects.filter(project_id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        serializer.save(project=Project.objects.get(pk=self.kwargs['project_id']))


class ProposalList(generics.ListCreateAPIView):
    permission_classes = (IsProjectOwner | IsEmployeeCreatingProposalForHerself, )
    serializer_class = ProposalSerializer

    def get_queryset(self):
        return Proposal.objects.filter(project_id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        serializer.save(project=Project.objects.get(pk=self.kwargs['project_id']))
