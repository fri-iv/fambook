from apps import socketio, app
import unittest
from libs.tools import log
from db import db_session
from apps.facebook.facebook_api import FacebookTestUser
import json


def callback(data):
    print 'callback:', data.data


class AuthClientClass:
    def __init__(self, auth_token=None):
        self.ws = socketio.test_client(app)
        self.token = auth_token

    def emit_request(self, url, data=None):
        import json

        try:
            resp = self.ws.emit(url, json.dumps(data), callback=callback)
            print '-------------------------------------'
            print url
            print 'raw response:', resp
            print 'resp type:', type(resp)
            from flask import Response
            if type(resp) == Response:
                print '(Response) data:', json.loads(resp.data)
                return json.loads(resp.data)
            else:
                print '(JSON) data:', json.loads(resp)
                return json.loads(resp)
        except Exception as JsonRequestError:
            log(JsonRequestError)

    def login(self):
        return self.emit_request('/api/v1/login', dict(access_token=self.token))

    def logout(self):
        return self.emit_request('/api/v1/logout')

    def delete(self):
        return self.emit_request('/api/v1/delete-me')


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.users_init_count = db_session.execute('SELECT COUNT(*) FROM users;').first()
        self.users_init_sess = db_session.execute('SELECT COUNT(*) FROM sessions;').first()

    def tearDown(self):
        users_count = db_session.execute('SELECT COUNT(*) FROM users;').first()
        sessions_count = db_session.execute('SELECT COUNT(*) FROM sessions;').first()

        assert self.users_init_count == users_count
        assert self.users_init_sess == sessions_count

    def test_auth(self):

        fb_user = FacebookTestUser('Yanukovych Viktor')
        auth = AuthClientClass(fb_user.access_token)

        response = auth.login()
        self.assertIn('id', response)

        response = auth.logout()
        print 'logout:', response
        self.assertIn('successfully', response)

        auth.login()
        response = auth.delete()
        self.assertIn('successfully', response)
