from django.urls import include, path

from .project_views import MilestoneList, ProjectList, ProposalList, ProjectDetail

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('project/<int:project_id>/milestones/', MilestoneList.as_view()),
    path('project/<int:project_id>/proposals/', ProposalList.as_view(), name='proposal-list'),
    path('projects/', ProjectList.as_view()),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
]
