import string
import random
from datetime import datetime
from itertools import chain

from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized
from tastypie.compat import User
from tastypie.paginator import Paginator

from task.models import Task, Project, TaskUser, TaskHistory
from . import ipc


class TaskPaginator(Paginator):
    def get_count(self):
        return 0

    def get_limit(self):
        limit = super(TaskPaginator, self).get_limit()
        status = self.request_data.get('status')

        # no status means we are doing the initial Active load
        # of all 3 swimlanes
        if status is None:
            limit = 60

        elif status == '0':
            limit = self.max_limit

        return limit

    def page(self):
        max_id = int(self.request_data.get('max_id', 0))

        objects = self.objects
        limit = self.get_limit()

        meta = {}

        if max_id:
            objects = objects.filter(id__lt=max_id)

        return {
            self.collection_name: objects[:limit],
            'meta': meta,
        }


class TokenAuthentication(Authentication):

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


class OrganizationTaskResource(ModelResource):
    created = fields.DictField(attribute='created')
    last_edited = fields.DictField(attribute='last_edited')
    project_id = fields.IntegerField(attribute='project_id')
    project = fields.CharField(attribute='project')

    class Meta:
        queryset = Task.objects.all()
        limit = 0
        resource_name = 'task'
        serializer = Serializer(["json"])
        always_return_data = True
        excludes = ['backlog_order', 'id']
        include_resource_uri = False


class OrganizationResource(ModelResource):
    tasks = fields.ToManyField('task.api.OrganizationTaskResource',
        lambda bundle: bundle.obj.task_set.filter(status=3),
        null = True,
        full = True)

    class Meta:
        queryset = TaskUser.objects.all()
        limit = 0
        resource_name = 'organization'
        serializer = Serializer(["json"])
        include_resource_uri = False
        filtering = {
            'id': ALL,
            'status': ALL,
            'assigned_to': ALL,
            'users': ALL_WITH_RELATIONS,
        }
        fields = ['email', 'tasks']
        always_return_data = True
        detail_allowed_methods = ['get', 'post', 'patch', 'put', 'delete']
        list_allowed_methods = ['get', 'patch', 'post', 'put', 'delete']
        authentication = TokenAuthentication()
        authorization = Authorization()


class TaskUserDetailResource(ModelResource):
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
        # include_resource_uri = False
        resource_name = 'assignee'
        authentication = TokenAuthentication()
        authorization = Authorization()
        serializer = Serializer(["json"])
        limit = 0
        detail_allowed_methods = []
        list_allowed_methods = ['get']
        fields = ['email', 'id']

    def obj_get_list(self, bundle, **kwargs):
        result = super(TaskUserResource, self) \
            .obj_get_list(bundle, **kwargs)
        result = result.filter(organization=bundle.request.user.organization)
        return result


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

    def obj_create(self, bundle, **kwargs):
        result = super(IPCModelResource, self) \
                .obj_create( bundle, skip_errors=False, **kwargs)

        ipc_handler = self.ipc_handler.__func__
        ipc_handler(bundle.obj, bundle.request.token, action='create')
        return result

    def obj_delete(self, bundle, **kwargs):
        result = super(IPCModelResource, self) \
                .obj_delete( bundle, **kwargs)

        ipc_handler = self.ipc_handler.__func__
        bundle.obj.id = kwargs['pk']
        ipc_handler(bundle.obj, bundle.request.token, action='delete')
        return result


class ProjectResource(IPCModelResource):
    ipc_handler = ipc.notify_project_update
    # tasks = fields.DictField(attribute='tasks')

    class Meta:
        queryset = Project.objects.all()
        limit = 0
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
        bundle = super(ModelResource, self).obj_create(*args, **kwargs)
        project = bundle.obj
        project.organization = bundle.request.user.organization
        project.users.add(bundle.request.user)
        project.save()
        return bundle

    def obj_update(self, bundle, **kwargs):
        bundle = super(self.__class__, self).obj_update(bundle, **kwargs)
        project = bundle.obj
        if bundle.data.get('user', False):
            project.users.add(bundle.request.user)
        return bundle

    def obj_delete(self, bundle, pk):
        # we dont want to delete the project,
        # just remove the user from the project
        project = Project.objects.get(id=pk)
        project.users.remove(bundle.request.user)

    def get_object_list(self, request):
        objects = self._meta.queryset._clone()
        if request.GET.get('all', False):
            return objects.filter(organization=request.user.organization) \
                          .exclude(users=request.user)
        else:
            return objects.filter(users=request.user)

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
                return data_dict


class TaskHistoryResource(ModelResource):
    class Meta:
        queryset = TaskHistory.objects.all()
        resource_name = 'taskhistory'
        serializer = Serializer(["json"])
        filtering = {
            'id': ALL,
            'status': ALL,
            'assigned_to': ALL,
            'users': ALL_WITH_RELATIONS,
        }


class TaskResource(IPCModelResource):
    project = fields.ForeignKey(
        'task.api.ProjectResource',
        'project', full=True, null=True)

    assigned_to = fields.ForeignKey(
        'task.api.TaskUserResource',
        'assigned_to', full=True, null=True)

    #created = fields.DictField(attribute='created')
    #last_edited = fields.DictField(attribute='last_edited')

    ipc_handler = ipc.notify_task_update

    class Meta:
        queryset = Task \
                   .objects \
                   .select_related('project', 'assigned_to') \
                   .all()
        limit = 20
        resource_name = 'task'
        serializer = Serializer(["json"])
        filtering = {
            #'label': ALL,
            #'description': ALL,
            'project': ALL_WITH_RELATIONS,
            'status': ALL,
            #'loe': ALL,
            #'task_type': ALL,
            #'assigned_to': ALL
        }

        always_return_data = True
        detail_allowed_methods = ['get', 'post', 'patch', 'put', 'delete']
        list_allowed_methods = ['get', 'patch', 'post', 'put', 'delete']
        authentication = TokenAuthentication()
        authorization = Authorization()
        paginator_class = TaskPaginator

    def apply_filters(self, request, applicable_filters):
        """
        An ORM-specific implementation of ``apply_filters``.

        The default simply applies the ``applicable_filters`` as ``**kwargs``,
        but should make it possible to do more advanced things.
        """
        objects = self.get_object_list(request)

        try:
            objects = objects.filter(**applicable_filters)
        except AttributeError:
            pass

        return objects

    def apply_sorting(self, obj_list, options=None):
        status = options.get('status')

        if status == '0':  # backlog
            # this is a problem.
            # you may not have all of the backlog
            # loaded, but you change the order of 1
            # we need a way to describe that or
            # backlog loads more tasks than the other guys

            fields = ('backlog_order',)
        elif status == '5':  # archived
            fields = ('-completed_on',)
        else:  # everythign else
            fields = ('-id',)

        try:
            return obj_list.order_by(*fields)
        except AttributeError:
            return obj_list

    def alter_deserialized_detail_data(self, request, data):
        if data.get('assigned_to', False) and not isinstance(data['assigned_to'], unicode):
            data['assigned_to'] = data['assigned_to']['resource_uri']
        return super(IPCModelResource, self).alter_deserialized_detail_data(request, data)

    def obj_update(self, bundle, **kwargs):
        bundle = super(ModelResource, self).obj_update(bundle, **kwargs)
        task = bundle.obj

        # TODO rework this sequence so we only call save() once
        if task.status == 3 and task.assigned_to is None:
            task.assigned_to = bundle.request.user
            task.save()

        if task.status == 4:  # moving from
            task.completed_on = datetime.utcnow()
            task.save()
        elif task.status == 5:
            if not task.completed_on:
                task.completed_on = datetime.utcnow()
                task.save()
        else:
            task.completed_on = None
            task.save()

        ipc_handler = self.ipc_handler.__func__
        ipc_handler(task, bundle.request.token)
        task_history = TaskHistory()
        task_history.task = task
        task_history.user = bundle.request.user
        task_history.save()
        return bundle

    def obj_create(self, bundle, **kwargs):
        result = super(TaskResource, self) \
            .obj_create( bundle, **kwargs)
        task = bundle.obj
        task_history = TaskHistory()
        task_history.task = task
        task_history.user = bundle.request.user
        task_history.save()
        return result

    def alter_detail_data_to_serialize(self, request, data):
        task = data.data
        task['project'] = task['project'].data['resource_uri']
        return data

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
                return data_dict
        objects = data_dict['objects']
        for obj in objects:
            task = obj.data
            task['project'] = task['project'].data['resource_uri']
        return data_dict

    def get_object_list(self, request):
        status = request.GET.get('status')

        # Clark was waking up, so I went cheap with request.method
        # here.
        if status or request.method != 'GET':
            return super(TaskResource, self).get_object_list(request)

        project_id = request.GET.get('project__id')

        # could probably just return a list and
        # handle applying the order and filters thouugh
        # tasty pie's notmal channels.
        #
        # would need to update self.apply_filters and
        # self.apply_sorting if we do that. They currently
        # handle the attribute error when their desired
        # property is not present and just forward this
        # list on.
        todo = self._meta.queryset._clone() \
            .filter(status=1, project__id=project_id) \
            .order_by('-id')[:20]

        in_progress = self._meta.queryset._clone() \
            .filter(status=3, project__id=project_id) \
            .order_by('-id')[:20]

        completed = self._meta.queryset._clone() \
            .filter(status=4, project__id=project_id) \
            .order_by('-id')[:20]

        return list(chain(todo, in_progress, completed))


class TokenResource(Resource):
    token = fields.CharField(attribute='token', null=True)
    ok = fields.BooleanField(attribute='ok')

    class Meta:
        include_resource_uri = False
        resource_name = 'token'
        serializer = Serializer(["json"])

    def obj_get(self, bundle, **kwargs):
        tokenResponse = ResponseObject({'ok': False})
        try:
            email = bundle.request.GET.get('u', False)
            password = bundle.request.GET.get('p', False)
            user = TaskUser.objects.get(email=email)
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
