from apps import app
from flask import request
from db import db_session
from decorators import login_required
from models import User
from libs.tools import ws_response, log


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
    print 'login func'
    user = User.login(request.sid, token)

    if not user:
        return ws_response(403, "Can't login")
    else:
        body = dict(
            name=user.name,
            id=user.id,
            photo=user.avatar_url
        )
        return ws_response(200, 'Login successfully', body)
        # print 'login in'


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
