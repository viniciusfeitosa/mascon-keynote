import json
import os


from nameko.rpc import rpc
from nameko.web.handlers import http
from nameko.standalone.rpc import ClusterRpcProxy

CONFIG = {'AMQP_URI': os.environ.get('QUEUE_HOST')}


class ApiService:

    name = 'ex2_api'

    @http('GET', '/sync/<int:id>')
    def get(self, request, id):
        content_type = {'Content-Type': 'application/json'}
        response = {}
        try:
            with ClusterRpcProxy(CONFIG) as cluster_rpc:
                response['first_name'] = cluster_rpc.ex2_domain1.task(id)
                response['last_name'] = cluster_rpc.ex2_domain2.task(id)
                response['twitter'] = cluster_rpc.ex2_domain3.task(id)
            return 200, content_type, json.dumps(response)
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
