from os import environ
from time import sleep
from typing import Optional

from tellopy._internal.error import TelloError

from .drone import TelloDrone
from .drone_data import DroneData
from .pilot import Pilot
from .video import Video

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class FlightAlreadyStartedException(Exception): pass


class DroneControl:
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
        print('Drone control run begin')

        self.drone_data = DroneData(self.pilot)
        self.drone.set_loglevel(self.drone.LOG_WARN)

        self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA, self.drone_data.event_handler)
        self.drone.subscribe(self.drone.EVENT_LOG_DATA, self.drone_data.event_handler)

        try:
            print("Connecting to drone...")
            self.drone.connect()
            self.drone.wait_for_connection(5)
            print("Connected to drone!")

            self.video.start()
            while self.running:
                sleep(0.01)
                if self.joystick_handler:
                    for event in pygame.event.get():
                        self.joystick_handler.handle_event(self.drone, event)
                # self.video.draw()
        except Exception as e:
            print('Drone control threw exception: ', e)
        finally:
            self.video.quit()
            self.drone.land()
            self.drone.quit()
            self.stop()
            print('Drone control run end')
