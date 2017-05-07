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
    access_token = None
    last_response = None

    def __init__(self):
        pass

    def request(self, method, endpoint='', params=None):
        if not params:
            params = dict()

        if self.access_token:
            params.update(dict(access_token=self.access_token))

        req = urllib2.Request(graph_url + endpoint + '?' + urllib.urlencode(params))
        # print graph_url + endpoint + '?' + urllib.urlencode(params)
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

    def test_user_create(self, name):

        name = name.strip()

        req = self.request('POST', APP_ID + '/accounts/test-users', dict(
            installed='true',
            name=name))
        return req

    def test_user_list(self):
        req = self.request('GET', APP_ID + '/accounts/test-users')
        return req

    def test_user_delete(self, user_id):

        req = self.request('DELETE', user_id)
        return req


class FacebookUser(FacebookBase):

    access_token = None
    name = None
    fb_id = None
    id = None

    def __init__(self, access_token):
        FacebookBase.__init__(self)
        self.access_token = access_token

        self.result = self.request('GET', 'me')
        self.name = self.result['name']
        self.fb_id = self.result['id']

    def __repr__(self):
        return "<FacebookUser({}, {})>".format(self.fb_id, self.name)


class FacebookTestUser(FacebookUser):

    app = None

    def __init__(self, name):

        self.app = FacebookApp()
        users = self.app.test_user_list()

        for user in users['data']:
            FacebookUser.__init__(self, user['access_token'])

            if self.name == name:
                break

        if self.name != name:
            print self.name + ' != ' + name
            user = self.app.test_user_create(name)
            FacebookUser.__init__(self, user['access_token'])

    def delete(self):
        self.app.test_user_delete(self.fb_id)


    def __repr__(self):
        return "<FacebookTestUser({}, {})>".format(self.fb_id, self.name)
