import json
from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms.models import model_to_dict

import zmq

STATUS_LIST = (
               (0, 'backlog'),
               (1, 'todo'),
               (2, 'accepted'),
               (3, 'in progress'),
               (4, 'completed'),
               (5, 'archived'),
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
class TaskUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class Organization(models.Model):
    label = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.label


class TaskUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254, blank=True, null=True)
    email = models.EmailField('email address', max_length=254, unique=True)
    token = models.CharField(max_length=254, blank=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)

    def __unicode__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = TaskUserManager()

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email




class Project(models.Model):
    label = models.CharField(max_length = 200)
    users = models.ManyToManyField(TaskUser, blank=True, null=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    def __unicode__(self):
        return self.label


class Task(models.Model):
    label = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=2000, blank=False, null=True)
    project = models.ForeignKey(Project)
    status = models.IntegerField(choices=STATUS_LIST, default=0)
    loe = models.IntegerField(choices=LOE, default=0)
    task_type = models.IntegerField(choices=TYPE, default=0)
    assigned_to = models.ForeignKey(TaskUser, blank=True, null=True)
    def assigned_email(self):
        return self.assigned_to.email


# @receiver(post_save, sender=Project)
# def notify_project_update(sender, instance, created, raw, **kwargs):
#     if created:
#         return
#     dic = model_to_dict(instance)
#     dic['organization_id'] = instance.organization.id
#     dic['project_id'] = instance.id
#     dic['type'] = 'project'
#     del dic['users']
#     model_json = json.dumps(dic)
#     c = zmq.Context()
#     s = c.socket(zmq.REQ)
#     ipc = 'ipc:///tmp/tasks_broker'
#     s.connect(ipc)
#     s.send(model_json)
#     s.recv()


# @receiver(post_save, sender=Task)
# def notify_task_update(sender, instance, created, raw, **kwargs):
#     if created:
#         return
#     dic = model_to_dict(instance)
#     dic['organization_id'] = instance.project.organization.id
#     dic['project_id'] = instance.project.id
#     dic['type'] = 'task'
#     model_json = json.dumps(dic)
#     c = zmq.Context()
#     s = c.socket(zmq.REQ)
#     ipc = 'ipc:///tmp/tasks_broker'
#     s.connect(ipc)
#     s.send(model_json)
#     s.recv()
