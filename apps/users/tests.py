from apps import socketio, app
import unittest
import json
from libs.tools import log
from db import db_session

TEST_FB_USER = 'EAAVSZCZBZCZCTvsBACHH5fqBZBfalOUy4HvZBz5MCK3ZBoZC4YGrrB3YyPhHZCAOvb3ozxr5I0Vg5MlHV9nEZAOycPRWo0NWt' \
               '7oT5c24U2GxL0v4VO0VXeruQZCbsggbZBnceBnVfl6otKypdpdUiEtGyZCLjorSjeSdHK1QFSGjLmXYCgA5oC9fzGn43o1psH9' \
               'ZA71ZA1k7ymZCYN3IdkuhYl6MtpW8Q78DbOJJCGxzOLl5MR3wiwZDZD'


class AuthClientClass:
    def __init__(self, auth_token=None):
        self.ws = socketio.test_client(app)
        self.user = None
        self.token = auth_token
        if not auth_token:
            self.token = TEST_FB_USER

    def emit_request(self, url, data=None):
        try:
            self.ws.emit(url, data)
            return self.ws.get_received()[0]['args'][0]
        except Exception as JsonRequestError:
            log(JsonRequestError)

    # def register(self):
    #     data = {
    #         'email': self.email,
    #         'password': self.password
    #     }
    #     return self.json_request('/api/v1/register', data=data)

    def login(self):
        return self.emit_request('/api/v1/login', self.token)

    def logout(self):
        return self.emit_request('/api/v1/logout')

    def delete(self):
        return self.emit_request('/api/v1/delete-me')


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.users_init_count = db_session.execute('SELECT COUNT(*) FROM users;').first()
        self.users_init_sess = db_session.execute('SELECT COUNT(*) FROM sessions;').first()
        self.auth = AuthClientClass(TEST_FB_USER)

    def tearDown(self):
        users_count = db_session.execute('SELECT COUNT(*) FROM users;').first()
        sessions_count = db_session.execute('SELECT COUNT(*) FROM sessions;').first()

        assert self.users_init_count == users_count
        assert self.users_init_sess == sessions_count

    def test_auth(self):
        # response = self.auth.login()
        # if response['details'] == 'Login or password is incorrect':
        #     response = self.auth.register()
        #     if response['details'] == 'User with same email already exists':
        #         raise
        #
        # response = self.auth.logout()
        # if response['details'] == 'You are not login in':
        #     raise

        response = self.auth.login()
        self.assertIn('id', response['body'])

        response = self.auth.logout()
        assert response['code'] == 200

        self.auth.login()
        response = self.auth.delete()
        print 'response:', response
        assert response['code'] == 200