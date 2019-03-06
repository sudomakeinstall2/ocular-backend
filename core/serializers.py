from rest_framework import serializers

from .models import Project, Milestone, Proposal


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ()


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        exclude = ()


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        exclude = ()

