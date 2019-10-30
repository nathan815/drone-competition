import logging
from time import sleep
from typing import Optional
import uuid
import pygame

from .joysticks import JoystickButtonHandler
from .database import CompetitionDatabase, get_cluster
from .drone import TelloDrone, DroneEventHandler
from .model import Pilot, Flight
from .video import Video
from .flight_config import FlightConfig

logger = logging.getLogger(__name__)
station_id = uuid.uuid3(uuid.NAMESPACE_URL, hex(uuid.getnode()))


class FlightAlreadyStartedException(Exception):
    def __init__(self):
        super().__init__('Flight is already started! Stop the current flight first.')


class FlightControl:
    def __init__(self,
                 flight_config: FlightConfig,
                 joystick_handler: JoystickButtonHandler,
                 pilot: Optional[Pilot] = None):

        self.running = False
        self.joystick_handler = joystick_handler
        self.drone_events: Optional[DroneEventHandler] = None
        self.pilot: Optional[Pilot] = pilot
        self.flight: Optional[Flight] = None
        self.flight_config = flight_config

        self.competition_db = None
        if flight_config.db_write_data:
            logger.info('Connecting to DSE Cluster...')
            self.competition_db = CompetitionDatabase(get_cluster())

        self.drone = TelloDrone(port=9001)
        self.video = Video(self.drone, self.drone_events)

    def stop(self):
        self.running = False
        self.video.stop()
        self.drone.land()
        self.drone.quit()

    def is_connected(self):
        return self.drone.connected.is_set()

    def run(self):

        if self.running:
            raise FlightAlreadyStartedException()

        self.flight = Flight(uuid.uuid1(), self.pilot, station_id)

        if self.flight_config.db_write_data:
            self.competition_db.insert_new_flight(self.flight)

        self.running = True

        logger.info('Flight control run begin')

        self.drone_events = DroneEventHandler(self.flight, self.flight_config, self.competition_db)
        self.drone.set_loglevel(self.drone.LOG_WARN)

        self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA, self.drone_events.handler)
        self.drone.subscribe(self.drone.EVENT_LOG_DATA, self.drone_events.handler)

        try:
            logger.info('Connecting to drone...')
            self.drone.connect()
            self.drone.wait_for_connection(5)
            logger.info('Connected to drone!')

            self.video.start()
            if self.flight_config.show_video_window:
                self.video.start_window_video_thread()

            # main loop
            while self.running:
                sleep(0.01)
                if self.joystick_handler:
                    for event in pygame.event.get():
                        self.joystick_handler.handle_event(self.drone, event)

        except Exception as e:
            logger.error(f'Flight control threw exception: {e}')
        finally:
            self.stop()
            logger.info('Flight control run ended')
