import json
import zmq
from django.forms.models import model_to_dict


IPC_ADDRESS = 'ipc:///tmp/tasks_broker'


def get_ipc():
    global IPC_ADDRESS

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(IPC_ADDRESS)
    return socket


def ipc_send(data):
    socket = get_ipc()
    socket.send(data)

    return socket.recv()


def notify_task_update(instance, token=None):
    dic = model_to_dict(instance)
    dic['organization_id'] = instance.project.organization.id
    dic['project_id'] = instance.project.id
    dic['type'] = 'task'

    data = json.dumps(dic)
    ipc_send(data)


def notify_project_update(instance, token=None):

    dic = model_to_dict(instance)
    dic['organization_id'] = instance.organization.id
    dic['project_id'] = instance.id
    dic['type'] = 'project'
    del dic['users']

    data = json.dumps(dic)
    ipc_send(data)
