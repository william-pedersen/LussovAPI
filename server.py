from io import FileIO
from posixpath import curdir
import threading, asyncio
from types import ModuleType
from flask import Flask
from flask_restful import Resource, Api, reqparse
import ast

from functools import wraps

from typing import ClassVar, List, Union, Optional
from enum import Enum, unique

import os
import itertools
import inspect, sys, importlib

import json

import pymongo, datetime
from bson import ObjectId
from pymongo.collection import ReturnDocument
import secrets



class Database(object):
    class Exceptions:
        class DuplicateUniqueError(Exception):
            pass

        class NotFoundError(Exception):
            pass

    def __init__(self) -> None:
        self.mongo = pymongo.MongoClient('MONGO CLIENT CONNECTION STRING')
        self.setup()

    def setup(self):
        pass

    def generateSession(self) -> str:
        return secrets.token_hex(48)

    




class Endpoint(Resource):
    class Codes(object):
        OK              = 200
        NOT_FOUND       = 404
        ERROR           = 500

    def __init__(self, app: Flask, api: Api, server: 'Server', url: Optional[str] = None) -> None:
        self.app        = app
        self.api        = api
        self.server     = server
        self.url        = url

    def RequiresAuth():
        def decorator(func):
            def wrapper(self, **kwargs):
                req = reqparse.RequestParser()
                req.add_argument('session', type=str, required = True)
                req.add_argument('uid', type=str, required = True)
                req.add_argument('content', type=str, required = True)
                _args = req.parse_args()
                args = {}
                return func(self, args = args)
            return wrapper
        return decorator

    def RequiresArgs():
        def decorator(func):
            def wrapper(self, **kwargs):
                req = reqparse.RequestParser()
                req.add_argument('content', type=str, required = True)
                args = dict(req.parse_args()).get('content', {})
                return func(self, args = json.loads(args))
            return wrapper
        return decorator

    def SecureAction():
        def decorator(func):
            def wrapper(self, **kwargs):
                req = reqparse.RequestParser()
                req.add_argument('content', type=str, required = True)
                args = dict(req.parse_args()).get('content', {})
                return func(self, args = json.loads(args))
            return wrapper
        return decorator





class Server(object):
    def __init__(self, 
        name: str = 'Server', 
        host: str = 'localhost', 
        port: Optional[Union[int, str]] = 5000,
        config: Optional[Union[str, dict]] = 'config.json', 
        apidir: Optional[str] = 'apis',
        **kwargs
    ) -> object:

        self.name = str(name)
        self.host = str(host)
        self.port = int(port)

        self.app = Flask(
            self.name
        )

        self.apidir = apidir

        with open(config, mode = 'r', encoding = 'UTF-8') as file:
            self.app.config.update(
                json.load(file)
            )

        self.database = Database(
            
        )

        endpoints = {
            endpoint : resources
            for endpoint
            in os.listdir(
                f'{os.curdir}/{self.apidir}'
            )
            if (
                resources := [
                    f'{os.curdir}/{self.apidir}/{endpoint}/{resource}'
                    for resource
                    in os.listdir(
                        f'{os.curdir}/{self.apidir}/{endpoint}'
                    )
                    if resource.endswith('.py')
                ]
            )
        }

        for endpoint, resources in endpoints.items():
            self.addRouting(
                endpoint = endpoint,
                resources = resources
            )

        [
            print(rule)
            for rule
            in self.app.url_map.iter_rules()
        ]

        self.app.run(
            host = self.host,
            port = self.port
        )

    def addRouting(self, endpoint: str, resources: list):
        api = Api(
            app = self.app,
            prefix = f'/{endpoint}'
        )

        for resource in resources:
            proto = importlib.util.find_spec(
                self.getResourceName(
                    (resource).lstrip('./').rstrip('.py').replace('/', '.')
                )
            )

            module = importlib.util.module_from_spec(proto)
            proto.loader.exec_module(module)

            [
                api.add_resource(
                    mod,
                    f'/{mod.__name__}'.lower(),
                    resource_class_kwargs = {
                        'app'       : self.app,
                        'api'       : api,
                        'server'    : self
                    }
                )
                for mod
                in tuple(getattr(
                        module,
                        'route'
                )()) + tuple([None])
                if (
                    hasattr(
                        module,
                        'route'
                    )
                ) and mod
            ]

    def addResource(self):
        pass

    def getEndpoints(self, proto: ModuleType) -> Optional[set]:
        module = importlib.util.module_from_spec(proto)
        proto.loader.exec_module(module)
        try:
            return getattr(
                module,
                'route'
            )()
        except AttributeError:
            return ()

    def getResource(self):
        pass

    def getResourceName(self, name: str, package: Optional[str] = None) -> str:
        try:
            return importlib.util.resolve_name(name, package)
        except ImportError as e:
            return None

    def getApi(self, app: Flask, _dir: Optional[str] = '', endpoint: Optional[str] = ''):
        api = Api(
            app = app,
            prefix = f'/{endpoint}'
        )
        protos = [
            module
            for file
            in
            os.listdir(
                f'{_dir}'
            )
            if file.endswith('.py') and (
                module := importlib.util.find_spec(
                    self.getResourceName(
                        (f'{_dir}/{file}').lstrip('./').rstrip('.py').replace('/', '.')
                    )
                )
            )
        ]
        endpoints = list(itertools.chain.from_iterable(
            [
                self.getEndpoints(
                    proto = proto
                )
                for proto
                in protos
            ]
        ))
        [
            api.add_resource(
                endpoint,
                urls = f'/{endpoint.__name__.lower()}',
                resource_class_kwargs = {
                    'app' : self.app,
                    'api' : api
                }
            )
            for endpoint
            in endpoints
        ]
        print(endpoints)
        return api

    def getAPI(self, _dir: str = '') -> Api:
        api = Api(
            app = self.app,
            prefix = '/' + _dir.split('/')[-1]
        )

        [
            api.add_resource(
                _endpoint,
                urls = f'/{_endpoint.__name__.lower()}',
                resource_class_kwargs = {
                    'app' : self.app,
                    'api' : api,
                    'url' : _endpoint.__name__.lower()
                }
            )
            for _endpoint
            in 
                [
                        _class[1]
                        for _class
                        in list(itertools.chain.from_iterable(
                            inspect.getmembers(
                                importlib.import_module(
                                    name = _endpoint[2:-3].replace('/', '.'),
                                    package = _endpoint[2:-3].replace('/', '.')
                                ),
                                inspect.isclass
                            )
                            for _endpoint
                            in [
                                f'{_dir}/{file}'
                                for file
                                in
                                os.listdir(
                                    f'{_dir}'
                                )
                                if file.endswith('.py')
                            ]
                        ))[1:]
                        if isinstance(
                            _class[1],
                            (type(Endpoint), Resource)
                        ) and (_class[0] != Endpoint.__name__ and _class[0] != Resource.__name__)
                        
                ]
        ]

        return api

    def addAPI(self, _dir: str = '', prefix: Optional[str] = None):
        self.apis += self.getAPI(
            _dir = _dir
        )

    def addEndpoint(self, api: Api, endpoint: object) -> None:
        match endpoint:
            case endpoint if isinstance(endpoint, (list, tuple, set)):
                [
                    self.addEndpoint(
                        api = api,
                        endpoint = e
                    )
                    for e
                    in endpoint
                    if endpoint is not None
                ]
            case endpoint if isinstance(endpoint, (Endpoint, Resource)):
                endpoint.__name__ = endpoint.url
                api.add_resource(
                    endpoint,
                    f'/{endpoint.url}',
                    
                )
            case _:
                print('Default')
        

def test():
    server = Server(
        
    )

if __name__ == '__main__':
    test()
