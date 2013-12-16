import json
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from txsockjs.factory import SockJSFactory
from txsockjs.utils import broadcast
from txzmq import ZmqEndpoint
from txzmq import ZmqFactory
from txzmq import ZmqREPConnection
from tastypie_driver import TastyPieDriver

transports = set()


class TasksProtocol(Protocol):

    def __init__(self):
        self.driver = TastyPieDriver()

    def connectionMade(self):
        print('connection started')
        transports.add(self.transport)

    def connectionLost(self, reason):
        print('connection closed')
        transports.remove(self.transport)

    def dataReceived(self, data):
        data = json.loads(data)
        action = getattr(self, data['action'])
        action(data['data'])

    def authorize(self, data):
        self.driver.authorize(data['token'], self.auth_callback);

    def auth_callback(self, data):
        data = json.loads(data)
        data = json.dumps(data['objects'][0])
        self.transport.write(data)


    def set_project(self, id):
        pass
        # will reset the locaiton of htis protocol


class TwistedRepConnection(ZmqREPConnection):
    def gotMessage(self, message_id, *messageParts):
        print('gotMessage')
        data = ''.join(messageParts)
        broadcast(data, transports)

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
