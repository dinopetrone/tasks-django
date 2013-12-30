import json
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory, Protocol
from txsockjs.factory import SockJSFactory
from txsockjs.utils import broadcast
from txzmq import ZmqEndpoint
from txzmq import ZmqFactory
from txzmq import ZmqREPConnection
from txzmq import ZmqEndpointType
from tastypie_driver import TastyPieDriver

transports = dict()


class TasksProtocol(Protocol):

    def __init__(self):
        self.key = None
        self.organization_id = None
        self.driver = TastyPieDriver()

    def connectionMade(self):
        print('connection started')

    def connectionLost(self, reason):
        print('connection closed')
        if self.key:
            transports[self.key].remove(self.transport)

    def dataReceived(self, data):
        data = json.loads(data)
        action = getattr(self, data['action'])
        action(data['data'])

    def authorize(self, data):
        self.driver.authorize(
            data['token'],
            self.auth_success_callback,
            self.auth_fail_callback)

    def auth_success_callback(self, data):
        data = json.loads(data)
        print(data)
        if data['organization']:
            self.organization_id = data['organization_id']

        out = {
            'ok': True,
            'data': data
        }
        self.transport.write(json.dumps(out))

    def auth_fail_callback(self, data):
        print(data)
        out = {
            'ok': False
        }
        self.transport.write(json.dumps(out))

    def set_project(self, data):
        if self.key:
            transports[self.key].remove(self.transport)
        project_id = data['project_id']
        self.key = '{}:{}'.format(self.organization_id, project_id)
        if not transports.get(self.key, False):
            transports[self.key] = set()
        transports[self.key].add(self.transport)
        # need to remove this transport from previous dictionary
        # will reset the locaiton of htis protocol


class TwistedRepConnection(ZmqREPConnection):
    def gotMessage(self, message_id, *messageParts):
        message = ''.join(messageParts)
        data = json.loads(message)
        key = '{}:{}'.format(data['organization_id'], data['project_id'])
        #print(key)
        #print(transports)
        channels = transports.get(key, False)
        if channels:
            broadcast(message, channels)

        self.reply(message_id, '')


def getZMQRepConnection(ipc_path):

    method = ZmqEndpointType.bind
    zf = ZmqFactory()
    e = ZmqEndpoint(method, ipc_path)
    return TwistedRepConnection(zf, e)


def getWSFactory():
    return SockJSFactory(Factory.forProtocol(TasksProtocol))


if __name__ == '__main__':
    zmq_connection = getZMQRepConnection('ipc:///tmp/tasks_broker')
    ws_factory = getWSFactory()

    endpoint = TCP4ServerEndpoint(reactor, 8888)
    endpoint.listen(ws_factory)

    reactor.run()
