import json

from ast import literal_eval

from nameko.events import EventDispatcher
from nameko.web.handlers import http
from nameko.events import event_handler
from nameko_redis import Redis


class ApiService:

    name = 'ex3_api'
    dispatch = EventDispatcher()
    redis = Redis('conn', encoding='utf-8')

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
            response = self.redis.get(uid)
            return 200, content_type, json.dumps(literal_eval(response))
        except Exception as e:
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
