import logging

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Milestone, Project, Proposal
from .serializers import (MilestoneSerializer, ProjectSerializer,
                          ProposalSerializer)

logger = logging.getLogger(__name__)


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        logger.info(request.user.pk)
        serializer.initial_data['user'] = request.user.pk
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MilestoneList(generics.ListCreateAPIView):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer


class ProposalList(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
