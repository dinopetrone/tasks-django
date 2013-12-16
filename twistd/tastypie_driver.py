from twisted.web.client import getPage

class TastyPieDriver(object):
    def authorize(self, token, callback):
        d = getPage(
                'http://localhost:8000/api/v1/user/',
                headers = {'Authorization': 'Bearer {}'.format(token)}
            )
        d.addCallback(callback)
