from twisted.internet import reactor
from txzmq import ZmqEndpoint
from txzmq import ZmqPubConnection, ZmqREPConnection
from txzmq import ZmqFactory


def initIPC():
    method = 'bind'
    endpoint = 'ipc:///tmp/tasks'

    zf = ZmqFactory()
    e = ZmqEndpoint(method, endpoint)

    p = ZmqPubConnection(zf, e)
    return p

def initResponse():
    method = 'bind'
    endpoint = 'ipc:///tmp/broker'
    zf = ZmqFactory()
    e = ZmqEndpoint(method, endpoint)
    r = TwistedRepConnection(zf, e)

    return r

class TwistedRepConnection(ZmqREPConnection):
    def gotMessage(self, message_id, *messageParts):
        self.publisher.publish(''.join(messageParts))
        self.reply(message_id, '')

if __name__ == '__main__':

    p = initIPC()
    r = initResponse()
    r.publisher = p
    reactor.run()



