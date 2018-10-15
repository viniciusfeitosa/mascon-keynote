import json

from nameko.events import EventDispatcher
from nameko.web.handlers import http
from nameko.events import event_handler
from nameko_redis import Redis


class ApiService:

    name = 'ex3.api'
    dispatch = EventDispatcher()
    redis = Redis('conn')

    @http('GET', '/async/<int:id>')
    def get(self, request, id):
        content_type = {'Content-Type': 'application/json'}
        try:
            self.dispatch('ex3.domain1.task', id)
            localtion = {
                'Location': 'http://localhost/async/{}/data'.format(id)
            } + content_type
            return 202, localtion, json.dumps({'status': 'ACCEPTED'})
        except Exception as e:
            return 500, content_type,  json.dumps({'error': e})

    @http('GET', '/async/<int:id>/data')
    def get_data(self, request, id):
        content_type = {'Content-Type': 'application/json'}
        try:
            response = self.redis.get(id)
            return 200, content_type, json.dumps(response)
        except Exception as e:
            return 202, content_type,  json.dumps({'status': 'PENDING'})


class Domain1:
    name = 'ex3.domain1'
    dispatch = EventDispatcher()

    @event_handler('ex3.api', 'ex3.domain1.task')
    def task(self, id):
        data = {'id', id}
        if id == 1:
            data['first_name'] = 'Vinicius'
        else:
            data['first_name'] = 'josé'
        self.dispatch('ex3.domain2.task', data)
