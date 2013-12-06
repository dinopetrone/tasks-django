from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from task.models import Task, Project
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication



class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project'
        serializer = Serializer(["json", "jsonp"])
        filtering = {
            'id': ALL,
            'status': ALL,
            'assigned_to': ALL,
        }
        detail_allowed_methods = ['get', 'post', 'patch', 'put']
        list_allowed_methods = ['get', 'patch', 'post', 'put']
        authentication = Authentication()
        authorization = Authorization()


class TaskResource(ModelResource):
    project = fields.ForeignKey('task.api.ProjectResource', 'project', full=True, null=True)
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        serializer = Serializer(["json", "jsonp"])
        filtering = {
            'label': ALL,
            'description': ALL,
            'project': ALL_WITH_RELATIONS,
            'status': ALL,
            'loe': ALL,
            'task_type': ALL,
            'assigned_to': ALL
        }
        detail_allowed_methods = ['get', 'post', 'patch', 'put']
        list_allowed_methods = ['get', 'patch', 'post', 'put']
        authentication = Authentication()
        authorization = Authorization()
