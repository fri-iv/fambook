from apps import app
import unittest
import json
from libs.tools import log
from db.db import db_session


class AuthClientClass:
    def __init__(self, email='test_user@fambook.com', password='password'):
        app.debug = True
        self.app = app.test_client()

        self.user = None
        self.email = email
        self.password = password

    def json_request(self, url, data=None):
        rv = None
        try:
            data = json.dumps(data)
            rv = self.app.post(url,
                               data=data,
                               follow_redirects=False,
                               content_type='application/json')
            return json.loads(rv.data)
        except Exception as JsonRequestError:
            error = '-------------------------\n' \
                    'UNDECODED JSON RESPONSE:{}\n'\
                    'URL:{}\n'\
                    'ERROR:{}\n'\
                    '-------------------------'.format(rv, url, JsonRequestError)
            log(error)

    def get_request(self, url, data=None):
        try:
            rv = self.app.get(url, follow_redirects=False)
            return json.loads(rv.data)
        except Exception as GetRequestError:
            log('get_request:' + str(GetRequestError))

    def register(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        return self.json_request('/api/v1/register', data=data)

    def login(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        return self.json_request('/api/v1/login', data=data)

    def logout(self):
        return self.get_request('/api/v1/logout')

    def delete(self):
        return self.get_request('/api/v1/delete-me')


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.users_init_count = db_session.execute('SELECT COUNT(*) FROM users;').first()
        self.users_init_sess = db_session.execute('SELECT COUNT(*) FROM sessions;').first()
        self.auth = AuthClientClass('test_user@fambook.com', 'password')

    def tearDown(self):
        users_count = db_session.execute('SELECT COUNT(*) FROM users;').first()
        sessions_count = db_session.execute('SELECT COUNT(*) FROM sessions;').first()

        print 'Users({}/{}), Sessions({}/{})'.format(self.users_init_count, users_count,
                                                     self.users_init_sess , sessions_count)
        assert self.users_init_count == users_count
        assert self.users_init_sess == sessions_count

    def test_register(self):
        response = self.auth.login()
        if response['details'] == 'Auth success':
            self.auth.delete()

        response = self.auth.register()
        assert response['details'] == 'New user created successfully'

        response = self.auth.register()
        assert response['details'] == 'User with same email already exists'

        response = self.auth.delete()
        assert response['details'] == 'User deleted'

    def test_logout(self):
        response = self.auth.logout()

        if response['details'] == 'Please, login in first':
            response = self.auth.login()
            if response['details'] == 'Login or password is incorrect':
                response = self.auth.register()
                if response['details'] == 'User with same email already exists':
                    raise
                self.auth.login()
        else:
            assert response['details'] == 'Logout successful'

        response = self.auth.logout()
        assert response['details'] == 'Logout successful'

        response = self.auth.logout()
        assert response['details'] == 'Please, login in first'

        self.auth.login()
        response = self.auth.delete()
        assert response['details'] == 'User deleted'

    def test_login(self):
        response = self.auth.login()
        if response['details'] == 'Login or password is incorrect':
            response = self.auth.register()
            if response['details'] == 'User with same email already exists':
                raise

        response = self.auth.logout()
        if response['details'] == 'You are not login in':
            raise

        response = self.auth.login()
        assert response['details'] == 'Auth success'

        response = self.auth.login()
        assert response['details'] == "You're already login in"

        response = self.auth.delete()
        assert response['details'] == 'User deleted'