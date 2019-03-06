from rest_framework import generics

from .models import Project, Milestone, Proposal
from .serializers import ProjectSerializer, MilestoneSerializer, ProposalSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MilestoneList(generics.ListCreateAPIView):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer


class ProposalList(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
