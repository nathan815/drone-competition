import threading
import time
from queue import Queue
from typing import Optional

from .commands import Command, CommandName
from ..core.flight_control import FlightControl, FlightAlreadyStartedException
from ..core.pilot import Pilot


class DroneEventThread(threading.Thread):

    def __init__(self):
        self._stop_request = threading.Event()
        self._commands = Queue()
        self._flight_control: Optional[FlightControl] = None
        self._runner_thread = None
        self._runner_thread_number = 0
        super().__init__(daemon=True, name='Drone Event Thread')

    def stop(self):
        self._stop_request.set()
        self.send(Command())  # queue a command to unblock the run loop

    def send(self, command: Command):
        self._commands.put(command)

    def get_video(self):
        return self._flight_control.video

    def run(self):
        self._flight_control = FlightControl()
        print('Drone event thread is starting')
        while not self._stop_request.is_set():
            time.sleep(0.01)
            command = self._commands.get(block=True)
            self._handle_command(command)
        print('Drone event thread is stopping')

    def _handle_command(self, command: Command):
        print('Executing ' + str(command.name))
        print('Data:', command.data)
        commands = {
            CommandName.SayHello: self._say_hello,
            CommandName.StartFlight: self._start_flight,
            CommandName.StopFlight: self._stop_flight
        }
        try:
            commands[command.name](command)
        except Exception as ex:
            print('Command exception: ', ex)

    def _say_hello(self, command: Command):
        print('Hello, ' + command.data['name'])

    def _start_flight(self, command: Command):
        if self._flight_control.running:
            raise FlightAlreadyStartedException()
        print('Starting flight...')
        pilot_info = command.data['pilot']
        print('Raw pilot data: ', pilot_info)
        pilot = Pilot(pilot_info.get('name'),
                      pilot_info.get('department'),
                      pilot_info.get('major'),
                      pilot_info.get('school'))
        print('Pilot: ', pilot)
        self._flight_control.pilot = pilot
        # execute the flight drone code in another thread
        # so we don't block our command processing loop
        name = f'Flight Control Run Thread {self._runner_thread_number}'
        self._runner_thread = threading.Thread(
            target=self._flight_control.start,
            name=name,
            daemon=True
        ).start()
        self._runner_thread_number += 1

    def _stop_flight(self, command: Command):
        print('Stop flight...')
        self._flight_control.stop()
