from nameko.events import EventDispatcher
from nameko.events import event_handler


class Domain2:
    name = 'ex3_domain2'
    dispatch = EventDispatcher()

    @event_handler('ex3_domain1', 'ex3_domain2.task')
    def task(self, data):
        if data['id'] == 1:
            data['last_name'] = 'Pacheco'
        else:
            data['last_name'] = 'Nadie'
        self.dispatch('ex3_domain3.task', data)
