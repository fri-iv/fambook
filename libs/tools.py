from flask import jsonify
import sys
import traceback
from json import loads
from flask_socketio import emit
from flask import request


def get_data(req):
    try:
        return loads(req.data)
    except:
        log()
        return None


def ws_response(status, details=None, body=None):
    emit(request.event['message'], {
        'code': status,
        'details': details,
        'body': body
    })


def json_response():
    pass


def log(text=None):
    print('ERROR: {}'.format(str(text)))
    traceback.print_exc(file=sys.stdout)
