from nameko.events import EventDispatcher
from nameko.events import event_handler


class Domain2:
    name = 'ex3.domain2'
    dispatch = EventDispatcher()

    @event_handler('ex3.domain1', 'ex3.domain2.task')
    def task(self, data):
        if id == 1:
            data['last_name'] = 'Pacheco'
        else:
            data['last_name'] = 'Nadie'
        self.dispatch('ex3.domain3.task', data)
