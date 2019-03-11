import logging

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from core.models import Project

logger = logging.getLogger(__name__)


class IsReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        project_id = view.kwargs['pk']
        return Project.objects.get(pk=project_id).owner == request.user


class IsProjectOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        project_id = view.kwargs['project_id']
        return Project.objects.get(pk=project_id).owner == request.user


class IsEmployeeCreatingProposalForHerself(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method != 'POST':
            return False

        return request.user.pk == int(request.data['user'])
