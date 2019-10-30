import logging
import threading
import time
from queue import Queue
from typing import Optional

from ..core.joysticks import JoystickButtonHandler
from .commands import Command, CommandName
from ..core.flight_control import FlightControl, FlightAlreadyStartedException, FlightConfig

logger = logging.getLogger(__name__)


class DroneEventThread(threading.Thread):

    def __init__(self):
        self._stop_request = threading.Event()
        self._commands = Queue()
        self._flight_control: Optional[FlightControl] = None
        self._runner_thread = None
        self._runner_thread_number = 0
        self._flight_config = FlightConfig(show_video_window=False)
        super().__init__(daemon=True, name='Web App Drone Event Thread')

    def stop(self):
        self._stop_request.set()
        self.send(Command())  # queue a command to unblock the run loop

    def send(self, command: Command):
        self._commands.put(command)

    def get_video(self):
        return self._flight_control.video

    def run(self):
        logger.info('Drone event thread is starting')
        self._flight_control = FlightControl(FlightConfig(), JoystickButtonHandler())
        while not self._stop_request.is_set() and self._flight_control.is_connected():
            time.sleep(0.1)
            command = self._commands.get(block=True)
            self._handle_command(command)
        self._flight_control.stop()
        logger.info('Drone event thread is stopping')

    def _handle_command(self, command: Command):
        logger.info('COMMAND: ' + str(command.name) +
                    ' - Data: ' + str(command.data))
        commands = {
            CommandName.SayHello: self._say_hello,
            CommandName.StartFlight: self._start_flight,
            CommandName.StopFlight: self._stop_flight
        }
        try:
            commands[command.name](command)
        except Exception as ex:
            logger.error(f'Command Exception: {str(ex)}')

    def _say_hello(self, command: Command):
        print('Hello, ' + command.data['name'])

    def _start_flight(self, command: Command):
        if self._flight_control.running:
            raise FlightAlreadyStartedException()
        logger.info('Starting flight...')
        pilot = command.data['pilot']
        logger.info('Pilot: ' + str(pilot))
        # execute the flight drone code in another thread
        # so we don't block our command processing loop
        name = f'Flight Control Run Thread {self._runner_thread_number}'
        self._flight_control.flight_config = self._flight_config
        self._runner_thread = threading.Thread(
            target=self._flight_control.run,
            name=name,
            daemon=True
        )
        self._runner_thread.start()
        self._runner_thread_number += 1

    def _stop_flight(self, _: Command):
        logger.info('Stop Flight')
        if self._flight_control:
            self._flight_control.stop()
