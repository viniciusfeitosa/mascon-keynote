import os

from time import sleep

from nameko.rpc import rpc
from redis import Redis

redis = Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)


class Domain3:
    name = 'ex2_domain3'

    @rpc
    def task(self, data):
        sleep(0.5)
        if data['id'] == 1:
            data['twitter'] = '@viniciuspach'
        else:
            data['twitter'] = '@nose'
        uid = 'ex2_{}'.format(data['id'])
        redis.set(uid, data)
