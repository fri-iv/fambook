from apps.users.models import Session
from flask import request
from db import db_session
from libs.tools import ws_error
from json import loads


def login_required(func):
    def inner(data=None):
        sess = db_session.query(Session).filter(Session.sid == request.sid).first()
        if sess:
            if data:
                return func(sess.user, loads(data))
            else:
                return func(sess.user)
        else:
            return ws_error(403,'Please, login in first')
    return inner
