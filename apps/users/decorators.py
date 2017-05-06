from functools import wraps
from apps.users.models import Session
from flask import session, request
from db import db_session
from libs.tools import ws_response


def login_required(func):
    def inner(data=None):
        sess = db_session.query(Session).filter(Session.sid == request.sid).first()
        if sess:
            if data:
                return func(sess.user, data)
            else:
                return func(sess.user)
        else:
            import json
            return json.dumps(dict(code=403, message='Please, login in first'))
    return inner
