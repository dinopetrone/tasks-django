import string
import random
import json
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from task.models import Task, Project, TaskUser



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
        always_return_data = True
        detail_allowed_methods = ['get', 'post', 'patch', 'put', 'delete']
        list_allowed_methods = ['get', 'patch', 'post', 'put', 'delete']
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
        always_return_data = True
        detail_allowed_methods = ['get', 'post', 'patch', 'put', 'delete']
        list_allowed_methods = ['get', 'patch', 'post', 'put', 'delete']
        authentication = Authentication()
        authorization = Authorization()


class TokenObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data

class TokenResource(Resource):
    token = fields.CharField(attribute='token', null=True)
    class Meta:
        include_resource_uri  = False
        resource_name = 'token'
        serializer = Serializer(["json"])
    def obj_get(self, bundle, **kwargs):
        pk = kwargs['pk']
        try:
            username = pk.split('/')[0]
            password = pk.split('/')[1]
            user = TaskUser.objects.get(username=username)
            is_valid = user.check_password(password)
        except TaskUser.DoesNotExist:
            return 'false'
        if is_valid:
            token = ''.join(random.choice(string.lowercase) for i in range(30))
            user.token = token
            user.save();
            return TokenObject({'token':token})
