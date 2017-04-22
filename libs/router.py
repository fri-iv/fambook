# -*- coding: utf-8 -*-
import yaml
from importlib import import_module
import sys
import os


def create_routs():
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    app = getattr(import_module('apps'), 'app')

    routed_apps = []
    # print os.walk('')
    for root, dirs, files in os.walk('apps/'):
        for _dir in dirs:
            for i in os.walk('apps/' + _dir):
                if 'routs.yml' in i[2]:
                    routed_apps.append(_dir)
    print '-------------'
    print 'paths: ', routed_apps

    # @app.route('/mark-item', methods=['POST'])
    # app.add_url_rule(‘/’, ‘hello’, hello_world)

    for yml_dir in routed_apps:
        stream = file('apps/' + yml_dir + '/routs.yml', 'r')
        print 'path:' + 'apps/' + yml_dir + '/routs.yml'
        routes = yaml.load(stream)

        for source in routes.keys():
            if source == 'api/':
                for version in routes[source].keys():
                    for rout in routes[source][version].keys():
                        for method in routes[source][version][rout].keys():
                            print method + '[' + routes[source][version][rout][method] + ']:' + source + version + rout
                            print 'loading view: apps/' + yml_dir + '.views.' + routes[source][version][rout][method]
                            _rout = routes[source][version][rout][method]
                            func = getattr(import_module('apps.' + yml_dir + '.views'), routes[source][version][rout][method])
                            app.add_url_rule('/', _rout, func)
                            # func = import_string('apps.notes.views.' + routes[source][version][rout][method])
                            print func
