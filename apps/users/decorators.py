from functools import wraps
from apps.users.models import Session
from flask import session, request
from db import db_session
from libs.tools import json_response, get_data


def login_required(func):
    @wraps(func)
    def inner():
        if 'token' in session:
            if session['token'] is not None:
                sess = db_session.query(Session).filter(Session.token == session['token']).first()
                if sess:
                    if request.method == 'POST':
                        return func(sess.user, get_data(request))
                    else:
                        return func(sess.user)

        return json_response(400, 'Please, login in first')
    return inner
