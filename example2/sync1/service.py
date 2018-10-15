import json
import os

from ast import literal_eval

from nameko.rpc import rpc
from nameko.web.handlers import http
from nameko.standalone.rpc import ClusterRpcProxy
from redis import Redis

CONFIG = {'AMQP_URI': os.environ.get('QUEUE_HOST')}
redis = Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)


class ApiService:

    name = 'ex2_api'

    @http('GET', '/sync/<int:id>')
    def get(self, request, id):
        content_type = {'Content-Type': 'application/json'}
        data = {'id': id}
        try:
            with ClusterRpcProxy(CONFIG) as cluster_rpc:
                data['first_name'] = cluster_rpc.ex2_domain1.task(id)
                data['last_name'] = cluster_rpc.ex2_domain2.task(id)
                cluster_rpc.ex2_domain3.task(data)
            uid = 'ex2_{}'.format(id)
            response = redis.get(uid).decode('utf-8')
            return 200, content_type, json.dumps(literal_eval(response))
        except Exception as e:
            return 500, content_type,  json.dumps({'error': e})


class Domain1:
    name = 'ex2_domain1'

    @rpc
    def task(self, id):
        if id == 1:
            return 'Vinicius'
        else:
            return 'Juan'
