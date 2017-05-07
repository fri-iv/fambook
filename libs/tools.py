from flask import jsonify
import sys
import traceback
from json import loads
from flask_socketio import emit
from flask import request
from apps.users.models import User
from db import db_session


def get_data(req):
    try:
        return loads(req.data)
    except:
        log()
        return None


def ws_response(status, details=None, body=None, event=None):
    # data = dict(code=status,
    #             details=details)
    # data.update(body)
    # emit(request.event['message'], data)
    # print data
    # emit(request.event['message'] if not event else event, {
    #     'code': status,
    #     'details': details,
    #     'body': body
    # })
    emit(request.event['message'] if not event else event, body)


def ws_callback(data=None):
    if not data:
        data = dict(
            successfully=True
        )
    return jsonify(data)


def ws_error(error, message):
    return jsonify(
        dict(
            error=error,
            message=message
        )
    )


def json_response():
    pass


def log(text=None):
    print('ERROR: {}'.format(str(text)))
    traceback.print_exc(file=sys.stdout)


def get_user_by_id(user_id):
    return db_session.query(User).filter(User.id == user_id).first()
