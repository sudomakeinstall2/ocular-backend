from django.urls import include, path

from .project_views import (AnswerDetail, MilestoneDetail, MilestoneList,
                            ProjectDetail, ProjectList, ProjectProposalList,
                            ProposalDetail, UserProposalList, SelfUserDetail, UserList, CommentList)

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('project/<int:project_id>/milestones/', MilestoneList.as_view(),
         name='milestone-list'),
    path('project/<int:project_id>/milestone/<int:pk>/', MilestoneDetail.as_view(),
         name='milestone-detail'),
    path('project/<int:project_id>/proposals/', ProjectProposalList.as_view(),
         name='project-proposal-list'),
    path('user/<int:pk>/proposals/', UserProposalList.as_view(),
         name='user-proposal-list'),
    path('projects/', ProjectList.as_view()),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('proposal/<int:pk>/', ProposalDetail.as_view(), name='proposal-detail'),
    path('answer/<int:pk>/', AnswerDetail.as_view(), name='answer-detail'),
    path('user/self/', SelfUserDetail.as_view(), name='self-user-detail'),
    path('users/', UserList.as_view(), name='users-list'),
    path('project/<int:pk>/comments/', CommentList.as_view(), name='comment-list'),
]
