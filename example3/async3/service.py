import logging
import os
import json

from time import sleep

from nameko.events import event_handler
from redis import Redis

redis = Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)


class Domain3:
    name = 'ex3_domain3'

    @event_handler('ex3_domain2', 'ex3_domain3.task')
    def task(self, data):
        sleep(0.5)
        if data['id'] == 1:
            data['twitter'] = '@viniciuspach'
        else:
            data['twitter'] = '@nose'
        uid = 'ex3_{}'.format(data['id'])
        logging.info('uid: {}'.format(uid))
        try:
            redis.set(uid, json.dumps(data))
        except Exception as e:
            logging.error(e)
