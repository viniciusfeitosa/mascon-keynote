import json
import os

from time import sleep

from nameko.web.handlers import http

CONFIG = {'AMQP_URI': os.environ.get('QUEUE_HOST')}


class ApiService:

    name = 'ex1.api'

    @http('GET', '/rock/<int:id>')
    def get(self, request, id):
        content_type = {'Content-Type': 'application/json'}
        response = {}
        try:
            d1 = Domain1()
            response['first_name'] = d1.task(id)
            d2 = Domain2()
            response['last_name'] = d2.task(id)
            d3 = Domain3()
            response['twitter'] = d3.task(id)
            return 200, content_type, json.dumps(response)
        except Exception as e:
            return 500, content_type, json.dumps({'error': e})


class Domain1:

    def task(self, id):
        if id == 1:
            return 'Vinicius'
        else:
            return 'Juan'


class Domain2:

    def task(self, id):
        if id == 1:
            return 'Pacheco'
        else:
            return 'Nadie'


class Domain3:

    def task(self, id):
        sleep(0.01)
        if id == 1:
            return '@viniciuspach'
        else:
            return '@nose'
