from django.core.management.base import BaseCommand
from task.models import TaskUser, Organization

class Command(BaseCommand):
    help = "Create a new superuser without prompting the user for input"

    def handle(self, *args, **options):
        organization = Organization()
        organization.label = 'blitz'
        organization.save();
        user = TaskUser(username="admin", email="admin@local.com",is_superuser=True, is_staff=True)
        user.set_password("pass")
        user.organization = organization

        user.save()

        self.stdout.write("Created admin: admin\n")
