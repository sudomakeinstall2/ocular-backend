import logging

from rest_framework import generics, permissions

from core.permissions import IsProjectOwner, IsReadOnly, IsEmployeeCreatingProposalForHerself, IsOwner, \
    HasAccessToProposal
from .models import Milestone, Project, Proposal
from .serializers import (MilestoneSerializer, ProjectSerializer,
                          ProposalSerializer)

logger = logging.getLogger(__name__)


class ProjectDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated | IsReadOnly, IsReadOnly | IsOwner)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MilestoneDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated | IsReadOnly, IsReadOnly | IsProjectOwner,)
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer


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
        project = Project.objects.get(pk=self.kwargs['project_id'])
        if self.request.user == project.owner:
            serializer.save(project=project, employer_accepted=True)
        elif self.request.user == serializer.validated_data['user']:
            serializer.save(project=project, employee_accepted=True)
        else:
            raise Exception("Unauthorized proposal creation")


class ProposalDetail(generics.RetrieveAPIView):
    permission_classes = (HasAccessToProposal, )
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
