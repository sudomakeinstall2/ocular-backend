from django.urls import include, path

from .project_views import MilestoneList, ProjectList, ProposalList

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('project/<int:project_id>/milestones/', MilestoneList.as_view()),
    path('project/<int:project_id>/proposals/', ProposalList.as_view(), name='proposal-list'),
    path('projects/', ProjectList.as_view()),
]
