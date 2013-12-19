from twisted.web.client import getPage

class TastyPieDriver(object):
    def authorize(self, token, success, fail):
        d = getPage(
                'http://localhost:8000/api/v1/user/me/',
                headers = {'Authorization': 'Bearer {}'.format(token)}
            )
        d.addCallback(success)
        d.addErrback(fail)

