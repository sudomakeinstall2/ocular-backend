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
    created = models.DateTimeField(auto_now_add=True)

    @property
    def owner(self):
        return self.project.owner

    def accepted(self):
        return self.employee_accepted and self.employer_accepted


class Answer(models.Model):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NOT_ANSWERED = "not_answered"
    ANSWER_STATE_CHOICES = (
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
        (NOT_ANSWERED, 'not_answered'),
    )

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, default=NOT_ANSWERED,
                             choices=ANSWER_STATE_CHOICES)
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
