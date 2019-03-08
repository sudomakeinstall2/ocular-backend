from rest_framework import serializers

from .models import Milestone, Project, Proposal


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

    class Meta:
        model = Proposal
        exclude = ()
