from django.utils import timezone
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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



class TaskUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField('email address', max_length=254, unique=True)
    token = models.CharField(max_length=254, blank=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    # date_joined = models.DateTimeField('date joined', default=timezone.now)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __unicode_self(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = TaskUserManager()





class Project(models.Model):
    label = models.CharField(max_length = 200)


class Task(models.Model):
    label = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=2000, blank=False)
    project = models.ForeignKey(Project)
    status = models.IntegerField(choices=STATUS_LIST, default=0)
    loe = models.IntegerField(choices=LOE, default=0)
    task_type = models.IntegerField(choices=TYPE, default=0)
    assigned_to = models.ForeignKey(TaskUser, blank=True, null=True)

