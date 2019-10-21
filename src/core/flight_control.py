import logging
from os import environ
from time import sleep
from typing import Optional

from .drone import TelloDrone
from .drone_data import DroneData
from .pilot import Pilot
from .video import Video

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

logger = logging.getLogger(__name__)


class FlightAlreadyStartedException(Exception):
    def __init__(self):
        super().__init__('Flight is already started')


class FlightControl:
    def __init__(self, pilot: Optional[Pilot] = None):
        self.running = False
        self.joystick_handler = None
        self.drone_data: Optional[DroneData] = None
        self.pilot: Optional[Pilot] = pilot
        self.drone = TelloDrone(port=9001)
        self.video = Video(self.drone, self.drone_data)

    def start(self):
        if self.running:
            raise FlightAlreadyStartedException()
        self.running = True
        self.run()

    def stop(self):
        self.running = False

    def run(self):
        logger.info('Drone control run begin')

        self.drone_data = DroneData(self.pilot)
        self.drone.set_loglevel(self.drone.LOG_WARN)

        self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA, self.drone_data.event_handler)
        self.drone.subscribe(self.drone.EVENT_LOG_DATA, self.drone_data.event_handler)

        try:
            logger.info("Connecting to drone...")
            self.drone.connect()
            self.drone.wait_for_connection(5)
            logger.info("Connected to drone!")

            self.video.start()
            while self.running:
                sleep(0.01)
                if self.joystick_handler:
                    for event in pygame.event.get():
                        self.joystick_handler.handle_event(self.drone, event)
        except Exception as e:
            logger.error(f'Drone control threw exception: {e}')
        finally:
            self.video.stop()
            self.drone.land()
            self.drone.quit()
            self.stop()
            logger.info('Drone control run end')
