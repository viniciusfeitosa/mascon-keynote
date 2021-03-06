import json
import logging
import os

from ast import literal_eval

from nameko.events import EventDispatcher
from nameko.web.handlers import http
from nameko.events import event_handler
from redis import Redis

redis = Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)


class ApiService:

    name = 'ex3_api'
    dispatch = EventDispatcher()

    @http('GET', '/async/<int:id>')
    def get(self, request, id):
        content_type = {'Content-Type': 'application/json'}
        try:
            self.dispatch('ex3_domain1.task', id)
            localtion = {
                'Location': 'http://localhost:8082/async/{}/data'.format(id)
            }
            header = {**localtion, **content_type}
            return 202, header, json.dumps({'status': 'ACCEPTED'})
        except Exception as e:
            return 500, content_type,  json.dumps({'error': e})

    @http('GET', '/async/<int:id>/data')
    def get_data(self, request, id):
        content_type = {'Content-Type': 'application/json'}
        try:
            uid = 'ex3_{}'.format(id)
            logging.info('uid: {}'.format(uid))
            response = redis.get(uid).decode('utf-8')
            logging.info(response)
            return 200, content_type, json.dumps(literal_eval(response))
        except Exception as e:
            logging.error(e)
            return 202, content_type,  json.dumps({'status': 'PENDING'})


class Domain1:
    name = 'ex3_domain1'
    dispatch = EventDispatcher()

    @event_handler('ex3_api', 'ex3_domain1.task')
    def task(self, id):
        data = {'id': id}
        if id == 1:
            data['first_name'] = 'Vinicius'
        else:
            data['first_name'] = 'Juan'
        self.dispatch('ex3_domain2.task', data)
