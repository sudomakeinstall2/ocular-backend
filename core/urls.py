from django.conf.urls import url

from .project_views import ProjectList, ProposalList, MilestoneList

urlpatterns = [
    url('projects/', ProjectList.as_view()),
    url('milestones/', MilestoneList.as_view()),
    url('proposals/', ProposalList.as_view()),
]
