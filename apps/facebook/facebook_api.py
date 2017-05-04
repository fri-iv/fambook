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


class Facebook:
    result = None
    app_token = None

    def __init__(self, token=''):
        self.token = token
        self.user_auth()

    def request(self, method, endpoint='', params=None):
        if not params:
            params = dict()

        if self.app_token:
            params.update(dict(access_token=self.app_token))
        # print method + ':' + graph_url + endpoint + '?' + urllib.urlencode(params)

        req = urllib2.Request(graph_url + endpoint, data=urllib.urlencode(params))
        req.get_method = lambda: method

        print req.get_method() + ':' + req.get_full_url() + '?' + req.get_data()

        try:
            result = urllib2.urlopen(req)
            return json.loads(result.read())
        except urllib2.HTTPError as e:
            data = json.loads(e.read())['error']
            print '<FacebookReqiestError[{}], Type[{}]: {}>'.format(str(e.code), data['type'], data['message'])
            return None


    def get_request(self, url, data=None):
        url = graph_url + url + ('?' if '?' not in url else '&') + 'access_token={}'.format(self.token)
        self.result = urllib2.urlopen(url)

        return json.loads(self.result.read())

    def app_auth(self, grant_type='client_credentials'):

        res = self.request('POST', 'oauth/access_token', dict(client_id=APP_ID,
                                                              client_secret=APP_SECRET,
                                                              grant_type=grant_type))
        self.app_token = res['access_token']
        return self.app_token

    def user_auth(self):
        try:
            self.result = self.get_request('me')
            print 'res2:', self.result
        except urllib2.HTTPError as e:
            raise AuthError


class FacebookTestUser(Facebook):
    def __init__(self):
        Facebook.__init__(self)
        self.app_auth()

    def test_user_create(self, name):

        req = self.request('POST', APP_ID + '/accounts/test-users', dict(
            installed='true',
            name=name))
        # import urllib
        #
        # data = dict(
        #     installed='true',
        #     name='Prosto Vasia',
        #     access_token=self.app_token
        # )
        # url = APP_ID + '/accounts/test-users'
        # print graph_url + url
        # print 'data:', urllib.urlencode(data)
        # req = urllib2.Request(graph_url + url, data=urllib.urlencode(data))
        # # req.add_header('Content-Type', 'application/json')
        # req.get_method = lambda: 'POST'
        # self.result = urllib2.urlopen(req)
        # print self.result
        # self.result = self.result.read()
        print req

    def test_user_list(self):
        req = self.request('POST', APP_ID + '/accounts/test-users')
        # url = APP_ID + '/accounts/test-users?access_token={}'.format(self.app_token)
        #
        # self.result = urllib2.urlopen(graph_url + url)
        # self.result = self.result.read()

        return req

    def test_user_delete(self, user_id):
        req = self.request('DELETE', APP_ID + '/accounts/test-users')

        # import urllib
        # data = dict(
        #     access_token=self.app_token
        # )
        # req = urllib2.Request(graph_url + user_id, data=urllib.urlencode(data))
        # req.get_method = lambda: 'DELETE'
        # self.result = urllib2.urlopen(req)
        # print self.result
        # self.result = self.result.read()
        print req