# -*- coding: utf-8 -*-
from yaml import load
from importlib import import_module
import sys
import os


_APPS_DIR_ = 'apps'
_ROUTS_NAME_ = 'routs'
_VIEWS_NAME_ = 'views'

app = getattr(import_module(_APPS_DIR_), 'socketio')


def _create_path(dict_route, route='', routes=None):
    if dict_route:
        for keys in dict_route.keys():
            if type(dict_route[keys]) == str:
                routes.append([route, keys, dict_route[keys]])
            else:
                _create_path(dict_route[keys], route + keys, routes=routes)


def map_rout(endpoint, _dir):
    func = getattr(import_module(_APPS_DIR_ + '.' + _dir + '.' + _VIEWS_NAME_), endpoint[2])
    # app.add_url_rule(rule='/' + endpoint[0], view_func=func, methods=[endpoint[1], ])
    app.on_event('/' + endpoint[0], func)


def create_routs(encoded_yml):
    _ROUTES_ = []
    _create_path(encoded_yml[0], routes=_ROUTES_)

    [map_rout(endpoint, encoded_yml[1]) for endpoint in _ROUTES_]


def load_routs():
    __APPS_PATH__ = _APPS_DIR_ + '/'

    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

    dirs = [_dir for _dir in os.listdir(__APPS_PATH__) if os.path.isdir(__APPS_PATH__ + _dir)]
    encoded_ymls = [[load(file(_APPS_DIR_ + '/' + _dir + '/' + _ROUTS_NAME_ + '.yml', 'r')), _dir] for _dir in dirs]

    map(create_routs, encoded_ymls)