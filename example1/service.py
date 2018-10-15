import json
import os

from ast import literal_eval
from time import sleep

from nameko.web.handlers import http
from redis import Redis

CONFIG = {'AMQP_URI': os.environ.get('QUEUE_HOST')}
redis = Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)


class ApiService:

    name = 'ex1.api'

    @http('GET', '/rock/<int:id>')
    def get(self, request, id):
        content_type = {'Content-Type': 'application/json'}
        data = {'id': id}
        try:
            d1 = Domain1()
            data['first_name'] = d1.task(id)
            d2 = Domain2()
            data['last_name'] = d2.task(id)
            d3 = Domain3()
            d3.task(data)
            uid = 'ex1_{}'.format(id)
            response = redis.get(uid).decode('utf-8')
            return 200, content_type, json.dumps(literal_eval(response))
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

    def task(self, data):
        sleep(0.5)
        if data['id'] == 1:
            data['twitter'] = '@viniciuspach'
        else:
            data['twitter'] = '@nose'
        uid = 'ex1_{}'.format(data['id'])
        redis.set(uid, data)
