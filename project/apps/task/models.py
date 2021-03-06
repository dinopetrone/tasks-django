from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.dateformat import format

STATUS_LIST = (
               (0, 'backlog'),
               (1, 'todo'),
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

    def tasks(self):
        output = {}
        tasks = self.task_set.all()
        for item in STATUS_LIST:
            output[item[0]] = tasks.filter(status=item[0]).count()
        return output


class Task(models.Model):
    label = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=2000, blank=False, null=True)
    project = models.ForeignKey(Project)
    status = models.IntegerField(choices=STATUS_LIST, default=0)
    loe = models.IntegerField(choices=LOE, default=0)
    task_type = models.IntegerField(choices=TYPE, default=0)
    assigned_to = models.ForeignKey(TaskUser, blank=True, null=True)
    backlog_order = models.IntegerField(default=0)
    completed_on = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.label

    def created(self):
        task_history = list(self.taskhistory_set.order_by('datetime')[:1])
        if task_history:
            task_history = task_history[0]

            return {
                "datetime":format(task_history.datetime, 'U'),
                "user_email":task_history.user.email
            }
        return {}

    def last_edited(self):
        task_history = list(self.taskhistory_set.order_by('datetime').reverse()[:1])
        if task_history:
            task_history = task_history[0]
            return {
                "datetime":format(task_history.datetime, 'U'),
                "user_email":task_history.user.email
            }
        return {}


class TaskHistory(models.Model):
    datetime = models.DateTimeField(auto_now=True, db_index=True)
    task = models.ForeignKey(Task)
    user = models.ForeignKey(TaskUser)
