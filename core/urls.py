from django.conf.urls import url

from .project_views import ProjectList, ProposalList, MilestoneList
from .views import signup, activate, login_view

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login_view, name='login'),
    url(r'^activate/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url('projects/', ProjectList.as_view()),
    url('milestones/', MilestoneList.as_view()),
    url('proposals/', ProposalList.as_view()),
]
