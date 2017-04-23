from apps import app
from flask import request
from db.db import db_session
from decorators import login_required
from models import User
from libs.tools import json_response, log


def register():
    from libs.tools import get_data

    try:
        resp = get_data(request.data)

        if not resp or not ('email' or 'password' in resp) or (not resp['email'] or not resp['password']):
            return json_response(400, 'Input data is incorrect')

        user = User.register(resp['email'], resp['password'])

        if not user:
            return json_response(400, 'User with same email already exists')

        db_session.commit()

        return json_response(200, 'New user created successfully')
    except Exception as e:
        log(e)
        return json_response(400, 'Input data is incorrect')


@login_required
def delete_me(user):
    try:
        if user.delete():
            return json_response(200, 'User deleted')
        return json_response(200, 'Could not delete this user')
    except Exception as DeleteWhileDeleting:
        db_session.rollback()
        log(DeleteWhileDeleting)
        return json_response(400, 'Could not delete this user')


def login():
    from libs.tools import get_data

    try:
        data = get_data(request.data)
        if not data or not ('email' or 'password' in data):
            return json_response(400, 'Input data is incorrect')

        res = User.login(data['email'], data['password'])
        if res == 2:
            return json_response(400, 'Login or password is incorrect')
        elif res == 1:
            return json_response(400, "You're already login in")
        else:
            return json_response(200, 'Auth success')
    except Exception as LoginError:
        log(LoginError)
        return json_response(400, 'Auth failed')


@login_required
def logout(user):
    try:
        if user.logout():
            return json_response(200, 'Logout successful')
        else:
            return json_response(200, 'You are not login in')
    except Exception as LogoutError:
        log(LogoutError)
        return json_response(200, 'Logout failed')
