class Command:
    def __init__(self, data: dict = {}):
        self.data = data

    def execute(self):
        pass


class SayHello(Command):
    def execute(self):
        print('Hello, ' + self.data['name'])


class StartTestFlight(Command):
    def execute(self):
        pass


class StopTestFlight(Command):
    def execute(self):
        pass
