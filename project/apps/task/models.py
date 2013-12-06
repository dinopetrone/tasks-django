from django.db import models
from django.contrib.auth.models import User

STATUS_LIST = (
               (0, 'backlog'),
               (1, 'accepted'),
               (2, 'in progress'),
               (3, 'completed'),
               (4, 'archived'),
               )


class Project(models.Model):
    title = models.CharField(max_length = 200)


class Task(models.Model):
    title = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=2000, blank=False)
    project = models.ForeignKey(Project)
    status = models.IntegerField(choices=STATUS_LIST, default=0)
    assigned_to = models.ForeignKey(User, blank=True, null=True)

