from time import sleep

from nameko.events import event_handler
from nameko_redis import Redis


class Domain3:
    name = 'ex3_domain3'
    redis = Redis('conn', encoding='utf-8')

    @event_handler('ex3_domain2', 'ex3_domain3.task')
    def task(self, data):
        sleep(0.01)
        if data['id'] == 1:
            data['twitter'] = '@viniciuspach'
        else:
            data['twitter'] = '@nose'
        uid = 'ex3_{}'.format(data['id'])
        self.redis.set(uid, data)
