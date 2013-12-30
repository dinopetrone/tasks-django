from twisted.application import service, internet
import twist


application = service.Application("Tasks IPC/WebSocket")

service = internet.TCPServer(8888, twist.getFactory())
service.setServiceParent(application)
