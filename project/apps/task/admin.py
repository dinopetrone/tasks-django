from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import TaskUser, Organization
from .forms import TaskUserChangeForm, TaskUserCreationForm

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
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = TaskUserChangeForm
    add_form = TaskUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'organization', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class OrganizationAdmin(admin.ModelAdmin):
    pass



admin.site.register(TaskUser, TaskUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
