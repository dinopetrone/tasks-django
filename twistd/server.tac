from twisted.application import service, internet
from twisted.python import log
import twist


# http://stackoverflow.com/questions/17265844/how-to-wrap-a-zeromq-bind-socket-in-a-twisted-application-service
class ZMQRepService(service.Service):
    ipc_path = 'ipc:///tmp/tasks_broker'

    def startService(self):
        log.msg('ZMQRepService starting on %s' % self.ipc_path)
        twist.getZMQRepConnection(self.ipc_path)

    def stopService(self):
        log.msg('ZMQRepService stopping on %s' % self.ipc_path)

application = service.Application("Tasks IPC/WebSocket")
service_collection = service.IServiceCollection(application)

zmq_service = ZMQRepService()
zmq_service.setServiceParent(service_collection)

ws_service = internet.TCPServer(8888, twist.getWSFactory())
ws_service.setServiceParent(service_collection)

'''
import zmq
import json
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("ipc:///tmp/tasks_broker")
data = {
'organization_id': 1,
'project_id': 9
}
socket.send(json.dumps(data))
socket.recv()
'''
