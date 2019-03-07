from django.conf.urls import url
from django.urls import include

from .project_views import MilestoneList, ProjectList, ProposalList

urlpatterns = [
    url('rest-auth/', include('rest_auth.urls')),
    url('rest-auth/registration/', include('rest_auth.registration.urls')),
    url('projects/', ProjectList.as_view()),
    url('milestones/', MilestoneList.as_view()),
    url('proposals/', ProposalList.as_view()),
]
