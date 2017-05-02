import urllib2
import json
from libs.tools import log

graph_url = "https://graph.facebook.com/v2.9/"
user_login_url = 'https://www.facebook.com/v2.9'
redirect_uri = 'https://www.facebook.com/connect/login_success.html'

APP_ID = '1498634080177915'
APP_SECRET = '9dcd6da409cb0ad415527a813fec7534'


class AuthError(Exception):
    pass


class Facebook:
    result = None

    def __init__(self, token=''):
        self.token = token
        self.user_auth()

    def get_request(self, url, data=None):
        url = graph_url + url + ('?' if '?' not in url else '&') + 'access_token={}'.format(self.token)
        self.result = urllib2.urlopen(url)

        return json.loads(self.result.read())

    # def pointer(self, grant_type='client_credentials'):
    #     url = '/oauth/access_token?client_id={}&client_secret={}&grant_type={}'.format(APP_ID, APP_SECRET, grant_type)
    #     req = self._request_(graph_url + url)
    #
    #     return req
    #
    # def app_auth(self):
    #     req = self._request_(graph_url + '/me')
    #
    #     return req

    def user_auth(self):
        try:
            self.result = self.get_request('me')
        except urllib2.HTTPError as e:
            log(e)
            raise AuthError

