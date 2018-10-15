from nameko.rpc import rpc


class Domain2:
    name = 'ex2.domain2'

    @rpc
    def task(self, id):
        if id == 1:
            return 'Pacheco'
        else:
            return 'Nadie'
