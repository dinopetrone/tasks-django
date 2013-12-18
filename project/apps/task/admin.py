from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import TaskUser, Organization, Project, Task
from .forms import TaskUserChangeForm, TaskUserCreationForm
from . import ipc


class TaskUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Organization'), {'fields': ('organization',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    form = TaskUserChangeForm
    add_form = TaskUserCreationForm

    list_display = (
        'email', 'first_name', 'last_name',
        'organization', 'is_staff')

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class IPCAdmin(admin.ModelAdmin):
    ipc_handler = None

    def save_model(self, request, obj, form, change):
        super(IPCAdmin, self).save_model(request, obj, form, change)

        # Get the unbound version of the function.
        # Going though self.ipc_handler retrieves the value
        # as a bound method (aka binds self as the first arg)
        # since it's retrieval is running though the class's
        # descriptor machinery

        ipc_handler = self.ipc_handler.__func__

        # An action from the admin effectively has no token.
        ipc_handler(obj, None)


class TaskAdmin(IPCAdmin):
    ipc_handler = ipc.notify_task_update


class ProjectAdmin(IPCAdmin):
    ipc_handler = ipc.notify_project_update

admin.site.register(TaskUser, TaskUserAdmin)
admin.site.register(Organization, admin.ModelAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
