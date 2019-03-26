import logging

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from core.permissions import (HasAccessToAnswer, HasAccessToProposal,
                              IsEmployeeCreatingProposalForHerself, IsOwner,
                              IsProjectOwner, IsReadOnly, IsSameUser)

from .models import Answer, Milestone, Project, Proposal
from .serializers import (AnswerSerializer, MilestoneSerializer,
                          ProjectSerializer, ProposalSerializer, UserSerializer)

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


class ProjectProposalList(generics.ListCreateAPIView):
    permission_classes = (IsProjectOwner | IsEmployeeCreatingProposalForHerself, )
    serializer_class = ProposalSerializer

    def get_queryset(self):
        return Proposal.objects.filter(project_id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_id'])
        proposal = serializer.save(project=project)
        if self.request.user == serializer.validated_data['user']:
            raise ValidationError("Can't create proposal for yourself!")
        if self.request.user == project.owner:
            Answer.objects.create(proposal=proposal, owner=serializer.validated_data['user'])
        elif self.request.user == serializer.validated_data['user']:
            Answer.objects.create(proposal=proposal, owner=project.owner)
        else:
            raise Exception("Unauthorized proposal creation")


class UserProposalList(generics.ListAPIView):
    permission_classes = (IsSameUser, )
    serializer_class = ProposalSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Proposal.objects.filter(Q(user__pk=user_id) | Q(project__owner__pk=user_id))


class ProposalDetail(generics.RetrieveAPIView):
    permission_classes = (HasAccessToProposal, )
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class AnswerDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (HasAccessToAnswer, )
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_update(self, serializer):
        answer = Answer.objects.get(pk=self.kwargs['pk'])
        if answer.state != Answer.NOT_ANSWERED:
            raise ValidationError(detail="Already answered.")
        serializer.save()


class SelfUserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        obj = User.objects.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj
