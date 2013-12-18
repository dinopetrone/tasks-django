import json
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from txsockjs.factory import SockJSFactory
from txsockjs.utils import broadcast
from txzmq import ZmqEndpoint
from txzmq import ZmqFactory
from txzmq import ZmqREPConnection
from tastypie_driver import TastyPieDriver

transports = dict()


class TasksProtocol(Protocol):

    def __init__(self):
        self.key = None
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
        self.driver.authorize(data['token'], self.auth_callback);

    def auth_callback(self, data):
        data = json.loads(data)
        data = data['objects'][0]

        if data['organization']:
            self.organization_id = data['organization_id']

        self.transport.write(json.dumps(data))


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
        print(key)
        print(transports)
        channels = transports.get(key, False)
        if channels:
            broadcast(message, channels)
        self.reply(message_id, '')


def initRep():
    method = 'bind'
    endpoint = 'ipc:///tmp/tasks_broker'
    zf = ZmqFactory()
    e = ZmqEndpoint(method, endpoint)
    print('initRep')
    return TwistedRepConnection(zf, e)


if __name__ == '__main__':
    factory = SockJSFactory(Factory.forProtocol(TasksProtocol))

    initRep()

    print('Starting Twisted Server')
    reactor.listenTCP(8888, factory)
    reactor.run()