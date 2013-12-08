import string
import random
import json
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from task.models import Task, Project, TaskUser, Organization


# class TaskAuthorization(Authorization):
#     def read_list(self, object_list, bundle):
#         token = bundle.request.GET['token']
#         user = TaskUser.objects.get(token=token)
#         # object_list = object_list
#         return object_list


class TaskUserResource(ModelResource):
    class Meta:
        queryset = TaskUser.objects.all()
        filtering = {
            'id': ALL,
        }


class ProjectResource(ModelResource):
    users = fields.ToManyField('task.api.TaskUserResource', 'users', null=True)
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project'
        serializer = Serializer(["json"])
        filtering = {
            'id': ALL,
            'status': ALL,
            'assigned_to': ALL,
            'users': ALL_WITH_RELATIONS,
        }
        always_return_data = True
        detail_allowed_methods = ['get', 'post', 'patch', 'put', 'delete']
        list_allowed_methods = ['get', 'patch', 'post', 'put', 'delete']
        authentication = Authentication()
        authorization = Authorization()
    def hydrate(self, bundle):
        # project = bundle.obj
        # token = bundle.request.GET['token']
        # # token = 'cxtmmrgxoeanpaxjsnxwiskdwieatx'
        # user = TaskUser.objects.get(token=token)
        # project.organization = user.organization
        # project.save()
        # project.users.add(user)
        return bundle

    def get_object_list(self, request):
        # token = request.GET.get('token', False)
        # # token = 'cxtmmrgxoeanpaxjsnxwiskdwieatx'
        # user = TaskUser.objects.get(token=token)
        # if request.GET.get('all', False):
        #     return Project.objects.filter(organization=user.organization)
        # else:
        #     return Project.objects.filter(users=user)
        import pdb; pdb.set_trace()
        return Project.objects.all()



class TaskResource(ModelResource):
    project = fields.ForeignKey('task.api.ProjectResource', 'project', full=True, null=True)
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        serializer = Serializer(["json"])
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
    ok = fields.BooleanField(attribute='ok')

    class Meta:
        include_resource_uri  = False
        resource_name = 'token'
        serializer = Serializer(["json"])
    def obj_get(self, bundle, **kwargs):
        tokenResponse = TokenObject({'ok':False})
        pk = kwargs['pk']
        try:
            username = pk.split('/')[0]
            password = pk.split('/')[1]
            user = TaskUser.objects.get(username=username)
            is_valid = user.check_password(password)
        except TaskUser.DoesNotExist:
            return tokenResponse
        if is_valid:
            token = ''.join(random.choice(string.lowercase) for i in range(30))
            user.token = token
            tokenResponse.token = token
            tokenResponse.ok = True
            user.save();
            return tokenResponse
