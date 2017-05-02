from apps import app, socketio
from flask.templating import render_template
from flask.app import session
from flask_socketio import send, emit
from flask import request
from libs.tools import ws_response




# def fb_login():
#     print 'sessions:', session
#     return render_template('facebook/templates/login.html')
#
#
# def show_fb_token():
#     print 'sessions:', session
#     return render_template('facebook/templates/show_tocken.html', **session)
#
#
# @socketio.on('connect')
# def socket_connected(json):
#     print 'sdfsf'
#     data = {
#         'output': 'connecting via socket'
#     }
#     send(data, json=True)
#
# @socketio.on('connect')
# def socket_connected(json):
#     print 'sdfsf'
#     data = {
#         'output': 'connecting via socket opa'
#     }
#     send(data, json=True)


@socketio.on('auth')
def handle_source(token):
    print 'token:', token
    from apps.users.models import User
    import json

    user = User.login(request.sid, token)

    if not user:
        ws_response('auth', 403)

    body = dict(
        name=user.name,
        id=user.id
    )

    ws_response('auth', 200, body)
    # return json.dumps(data)
