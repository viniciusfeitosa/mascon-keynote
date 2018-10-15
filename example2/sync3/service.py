from time import sleep

from nameko.rpc import rpc


class Domain3:
    name = 'ex2_domain3'

    @rpc
    def task(self, id):
        sleep(0.5)
        if id == 1:
            return '@viniciuspach'
        else:
            return '@nose'
