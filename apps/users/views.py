from apps import app
from flask import request
from db import db_session
from decorators import login_required
from models import User
from libs.tools import ws_response, log


def register():
    from libs.tools import get_data

    try:
        resp = get_data(request)

        if not resp or not ('email' or 'password' in resp) or (not resp['email'] or not resp['password']):
            return ws_response(400, 'Input data is incorrect')

        user = User.register(resp['email'], resp['password'])

        if not user:
            return ws_response(400, 'User with same email already exists')

        db_session.commit()

        return ws_response(200, 'New user created successfully')
    except Exception as e:
        log(e)
        return ws_response(400, 'Input data is incorrect')


@login_required
def delete_me(user):
    try:
        if user.delete():
            return ws_response(200, 'User deleted')
        return ws_response(200, 'Could not delete this user')
    except Exception as DeleteWhileDeleting:
        db_session.rollback()
        log(DeleteWhileDeleting)
        return ws_response(400, 'Could not delete this user')


def login(token):
    user = User.login(request.sid, token)

    if not user:
        ws_response(403)
    else:
        body = dict(
            name=user.name,
            id=user.id
        )
        ws_response(200, body)


@login_required
def logout(user):
    try:
        if user.logout():
            return ws_response(200, 'Logout successful')
        else:
            return ws_response(403, 'You are not login in')
    except Exception as LogoutError:
        log(LogoutError)
        return ws_response(400, 'Logout failed')
