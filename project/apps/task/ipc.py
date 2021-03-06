import json
import zmq
from django.forms.models import model_to_dict
from django.utils.dateformat import format

IPC_ADDRESS = 'ipc:///tmp/tasks_broker'


def ipc_connection():
    global IPC_ADDRESS

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(IPC_ADDRESS)
    return socket


def ipc_send(data):
    socket = ipc_connection()
    socket.send(data)

    return socket.recv()


def notify_task_update(instance, token=None, action='update'):
    dic = model_to_dict(instance)

    dic['organization_id'] = instance.project.organization.id
    dic['project_id'] = instance.project.id
    dic['project_label'] = instance.project.label
    dic['assigned_to'] = {}
    if instance.assigned_to:
        dic['assigned_to']['email'] = instance.assigned_to.email
    dic['type'] = 'task'
    dic['token'] = token
    dic['id'] = instance.id
    dic['action'] = action
    dic['backlog_order'] = instance.backlog_order

    if(instance.completed_on):
        dic['completed_on'] = format(instance.completed_on, 'U')

    data = json.dumps(dic)
    ipc_send(data)


def notify_project_update(instance, token=None, action='update'):

    dic = model_to_dict(instance)
    dic['organization_id'] = instance.organization.id
    dic['project_id'] = instance.id
    dic['type'] = 'project'
    dic['token'] = token
    dic['action'] = action
    del dic['users']

    data = json.dumps(dic)
    ipc_send(data)
