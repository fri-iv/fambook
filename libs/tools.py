from flask import jsonify
import sys
import traceback
from json import loads


def get_data(req):
    return loads(req.data)


def json_response(status, details, body=None):
    return jsonify({
        'status': status,
        'details': details,
        'body': body
    })


def log(text=None):
    print('ERROR: {}'.format(str(text)))
    traceback.print_exc(file=sys.stdout)
