from django.db import models
from django.contrib.auth.models import User

STATUS_LIST = (
               (0, 'backlog'),
               (1, 'accepted'),
               (2, 'in progress'),
               (3, 'completed'),
               (4, 'archived'),
               )


LOE = (
    (0, 'low'),
    (1, 'medium'),
    (2, 'high'),
)

TYPE = (
    (0, 'task'),
    (1, 'bug')
)

class Project(models.Model):
    label = models.CharField(max_length = 200)


class Task(models.Model):
    label = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=2000, blank=False)
    project = models.ForeignKey(Project)
    status = models.IntegerField(choices=STATUS_LIST, default=0)
    loe = models.IntegerField(choices=LOE, default=0)
    task_type = models.IntegerField(choices=TYPE, default=0)
    assigned_to = models.ForeignKey(User, blank=True, null=True)

