from tastypie.resources import ModelResource, ALL
from task.models import Task, Project
from tastypie.serializers import Serializer


class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        serializer = Serializer(["json", "jsonp"])
        filtering = {
            'project': ALL,
            'status': ALL,
            'assigned_to': ALL,
        }

class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project'
        serializer = Serializer(["json", "jsonp"])
        filtering = {
            'project': ALL,
            'status': ALL,
            'assigned_to': ALL,
        }
