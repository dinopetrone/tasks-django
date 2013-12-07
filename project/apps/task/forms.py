from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from task.models import TaskUser

class TaskUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(TaskUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = TaskUser
        fields = ("email",)

class TaskUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(TaskUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = TaskUser
