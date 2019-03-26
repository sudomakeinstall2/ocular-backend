from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Answer, Milestone, Project, Proposal


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Project
        exclude = ()


class MilestoneSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.title')

    class Meta:
        model = Milestone
        exclude = ()


class ProposalSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.title')
    answer = serializers.ReadOnlyField(source='answer.id')

    class Meta:
        model = Proposal
        exclude = ()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id')
