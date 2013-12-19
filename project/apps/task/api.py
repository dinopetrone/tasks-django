import string
import random

from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized
from tastypie.compat import User
from django.forms.models import model_to_dict

from task.models import Task, Project, TaskUser
from . import ipc

class TokenAuthentication(Authorization):

    def get_identifier(self, request):
        return request.user.email

    def _unauthorized(self):
        response = HttpUnauthorized()
        return response

    def is_authenticated(self, request, **kwargs):
        try:
            type, token = request.META.get('HTTP_AUTHORIZATION').split()
        except:
            return self._unauthorized()
        if not token:
            return self._unauthorized()

        try:
            user = TaskUser.objects.get(token=token)

        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return self._unauthorized()

        request.user = user
        request.token = token
        return True


class ResponseObject(object):
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


class TaskUserDetailResource(ModelResource):
    username = fields.CharField(attribute='username')
    first_name = fields.CharField(attribute='first_name')
    last_name = fields.CharField(attribute='last_name')
    organization = fields.CharField(attribute='organization')
    organization_id = fields.CharField(attribute='organization_id')

    class Meta:
        include_resource_uri = False
        resource_name = 'user'
        authentication = TokenAuthentication()
        authorization = Authorization()
        serializer = Serializer(["json"])

    def obj_get(self, bundle, **kwargs):
        return bundle.request.user



class TaskUserResource(ModelResource):
    class Meta:
        queryset = TaskUser.objects.all()
        filtering = {
            'id': ALL,
        }


class IPCModelResource(ModelResource):
    ipc_handler = None

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        result = super(IPCModelResource, self) \
            .obj_update(bundle, skip_errors, **kwargs)

        # Get the unbound version of the function.
        # Going though self.ipc_handler retrieves the value
        # as a bound method (aka binds self as the first arg)
        # since it's retrieval is running though the class's
        # descriptor machinery
        ipc_handler = self.ipc_handler.__func__
        ipc_handler(bundle.obj, bundle.request.token)

        return result


class ProjectResource(IPCModelResource):
    # users = fields.ToManyField('task.api.TaskUserResource', 'users', null=True)
    ipc_handler = ipc.notify_project_update

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
        authentication = TokenAuthentication()
        authorization = Authorization()

    def obj_create(self, *args, **kwargs):
        bundle = super(self.__class__, self).obj_create( *args, **kwargs)
        project = bundle.obj
        project.organization = bundle.request.user.organization
        project.users.add(bundle.request.user)
        project.save()
        return bundle


    def obj_update(self, bundle, **kwargs):
        bundle = super(self.__class__, self).obj_update( bundle, **kwargs)
        project = bundle.obj
        if bundle.data.get('user', False):
            project.users.add(bundle.request.user)
        return bundle


    def obj_delete(self, bundle, pk):
        # we dont want to delete the project,
        # just remove the user from the project
        project = Project.objects.get(id=pk)
        project.users.remove(bundle.request.user)

    def obj_save(self, bundle):
        print('hi')
        super(ProjectResource, self).obj_save(self, bundle)


    def get_object_list(self, request):
        objects = self._meta.queryset._clone()
        if request.GET.get('all', False):
            return objects.filter(organization=request.user.organization)
        else:
            return objects.filter(users=request.user)


class TaskResource(IPCModelResource):
    project = fields.ForeignKey('task.api.ProjectResource', 'project', full=True, null=True)
    ipc_handler = ipc.notify_task_update

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
        authentication = TokenAuthentication()
        authorization = Authorization()

    def alter_deserialized_detail_data(self, request, data):
        data['assigned_to'] = request.user.id
        return data

    def dehydrate(self, bundle):
        task = bundle.obj
        if task.status == 2:
            task.assigned_to = bundle.request.user
            task.save()
        return bundle

    def alter_detail_data_to_serialize(self, request, data):
        task = data.data
        task['project'] = task['project'].data['resource_uri']
        return data

    def alter_list_data_to_serialize(self, request, data):
        objects = data['objects']
        for obj in objects:
            task = obj.data
            task['project'] = task['project'].data['resource_uri']
        return data





class TokenResource(Resource):
    token = fields.CharField(attribute='token', null=True)
    ok = fields.BooleanField(attribute='ok')

    class Meta:
        include_resource_uri = False
        resource_name = 'token'
        serializer = Serializer(["json"])

    def obj_get(self, bundle, **kwargs):
        tokenResponse = ResponseObject({'ok': False})
        pk = kwargs['pk']
        try:
            username = pk.split('/')[0]
            password = pk.split('/')[1]
            user = TaskUser.objects.get(username=username)
            is_valid = user.check_password(password)
        except Exception:
            return tokenResponse
        if is_valid:
            token = ''.join(random.choice(string.lowercase) for i in range(30))
            user.token = token
            tokenResponse.token = token
            tokenResponse.ok = True
            user.save()
            return tokenResponse
