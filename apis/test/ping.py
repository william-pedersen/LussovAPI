import sys
from typing import Optional
sys.path.append('.')

from server import Endpoint
from flask_restful import Resource, Api, reqparse
import requests


class Ping(Endpoint):
    def __init__(self, **kwargs) -> Endpoint:
        super().__init__(**kwargs)

    @Endpoint.RequiresArgs()
    def get(self, args: dict) -> tuple:
        print(args)

        return {'response' : 'Pong'}, Endpoint.Codes.OK

class Test(Endpoint):
    def __init__(self, **kwargs) -> Endpoint:
        super().__init__(**kwargs)

    def get(self) -> tuple:

        return {}, Endpoint.Codes.OK

#Ping()

def route() -> Optional[set]:
    return [
        Ping,
        Test
    ]
