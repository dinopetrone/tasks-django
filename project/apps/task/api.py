from tastypie.resources import ModelResource, ALL
from task.models import Task, Project
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication


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
        detail_allowed_methods = ['get', 'post', 'patch', 'put']
        list_allowed_methods = ['get', 'patch', 'post', 'put']
        authentication = Authentication()
        authorization = Authorization()

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
        detail_allowed_methods = ['get', 'post', 'patch', 'put']
        list_allowed_methods = ['get', 'patch', 'post', 'put']
        authentication = Authentication()
        authorization = Authorization()
