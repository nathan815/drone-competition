from datetime import datetime
import time
import threading
from queue import Queue
from .commands import Command


class DroneThread(threading.Thread):

    def __init__(self):
        self._running = True
        self._commands = Queue()
        threading.Thread.__init__(self, daemon=True, name='Drone Thread')

    def request_stop(self):
        self._running = False
        self.send_command(Command())  # queue a command to unblock the run loop

    def send_command(self, command: Command):
        self._commands.put(command)

    def run(self):
        print('Drone thread is starting')
        while self._running:
            time.sleep(0.1)
            command = self._commands.get(block=True)
            self._handle_command(command)
        print('Drone thread is stopping')

    def _handle_command(self, command: Command):
        print('Executing ' + command.__class__.__name__)
        print('Data:', command.data)
        command.execute()
