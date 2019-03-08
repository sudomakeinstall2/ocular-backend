from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(blank=False, max_length=300)
    description = models.TextField()
    deadline = models.DateField()
    cost = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deadline = models.DateField()
    title = models.CharField(blank=False, max_length=300)
    description = models.TextField()

    @property
    def owner(self):
        return self.project.owner


class Proposal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    cost = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    employer_accepted = models.BooleanField(default=False)
    employee_accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def owner(self):
        return self.project.owner

    def accepted(self):
        return self.employee_accepted and self.employer_accepted
