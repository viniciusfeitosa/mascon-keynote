from time import sleep

from nameko.events import event_handler
from nameko_redis import Redis


class Domain3:
    name = 'ex3.domain3'
    redis = Redis('conn')

    @event_handler('ex3.domain2', 'ex3.domain3.task')
    def task(self, data):
        sleep(0.01)
        if id == 1:
            data['twitter'] = '@viniciuspach'
        else:
            data['twitter'] = '@nose'
        self.redis.set(data['id'], data)
