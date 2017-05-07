from apps import app
from flask import request
from decorators import login_required
from models import User
from libs.tools import ws_response, ws_callback, ws_error


@login_required
def delete_me(user, data=None):

    if user.delete():
        return ws_callback()

    return ws_error(400, 'Could not delete this user')


def login(data):
    import json

    token = json.loads(data)['access_token']
    print token
    user = User.login(request.sid, token)

    if not user:
        return ws_error(400, "Can't login in")

    body = dict(
        name=user.name.encode('utf-8'),
        id=user.id,
        photo=user.avatar_url
    )

    return ws_callback(body)


@login_required
def logout(user, data=None):

    if user.logout():
        return ws_callback()

    return ws_error(400, 'Unexpected error')