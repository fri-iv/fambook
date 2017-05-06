import urllib, urllib2
import json
# from libs.tools import log

graph_url = "https://graph.facebook.com/v2.9/"
# user_login_url = 'https://www.facebook.com/v2.9'
# redirect_uri = 'https://www.facebook.com/connect/login_success.html'

APP_ID = '1498634080177915'
APP_SECRET = '9dcd6da409cb0ad415527a813fec7534'


class AuthError(Exception):
    pass


class FacebookBase:
    app_token = None
    last_response = None

    def __init__(self):
        pass

    def request(self, method, endpoint='', params=None):
        if not params:
            params = dict()

        if self.app_token:
            params.update(dict(access_token=self.app_token))

        req = urllib2.Request(graph_url + endpoint + '?' + urllib.urlencode(params))
        req.get_method = lambda: method

        try:
            self.last_response = urllib2.urlopen(req)
            return json.loads(self.last_response.read())
        except urllib2.HTTPError as e:
            data = json.loads(e.read())['error']
            print '<FacebookRequestError[{}], Type[{}]: {}>'.format(str(e.code), data['type'], data['message'])
            raise AuthError
            # return None


class FacebookApp(FacebookBase):

    def __init__(self, grant_type='client_credentials'):
        FacebookBase.__init__(self)

        req = self.request('POST', 'oauth/access_token', dict(client_id=APP_ID,
                                                              client_secret=APP_SECRET,
                                                              grant_type=grant_type))
        self.access_token = req['access_token']


class FacebookUser(FacebookBase):

    access_token = None
    name = None
    fb_id = None

    def __init__(self, access_token):
        FacebookBase.__init__(self)
        FacebookBase.access_token = access_token

        self.result = self.request('GET', 'me')


class FacebookTestUser:

    access_token = None
    fb_user_id = None
    name = None

    c_app = None
    c_user = None

    def __init__(self, name=None):
        self.c_app = FacebookApp()

        if name:
            user = self.get_user(name)

    def get_user(self, name):
        users = self.test_user_list()
        print 'users:', users

        for user in users['data']:
            u = FacebookUser(user['access_token'])
            if u.name == name:
                self.access_token = user['access_token']
                return u

        res = self._test_user_create(name)
        print 'created :', res

    def _test_user_create(self, name):

        name = name.strip()

        req = self.c_app.request('POST', APP_ID + '/accounts/test-users', dict(
            installed='true',
            name=name))
        return req

    def test_user_list(self):
        print 'app token:', self.c_app.access_token
        req = self.c_app.request('GET', APP_ID + '/accounts/test-users')
        return req

    def _test_user_delete(self, user_id):

        req = self.c_app.request('DELETE', user_id)
        return req
