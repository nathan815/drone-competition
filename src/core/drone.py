from typing import Optional

from tellopy import Tello
from datetime import datetime

from .flight_config import FlightConfig
from .database import CompetitionDatabase
from .model import Flight, FlightPosition


class TelloDrone(Tello):
    throttle = 0.0
    yaw = 0.0
    pitch = 0.0
    roll = 0.0

    def set_throttle(self, value):
        self.throttle = self._update(self.throttle, value)
        super().set_throttle(self.throttle)

    def set_yaw(self, value):
        self.yaw = self._update(self.yaw, value)
        super().set_yaw(self.yaw)

    def set_pitch(self, value):
        self.pitch = self._update(self.pitch, value)
        super().set_pitch(self.pitch)

    def set_roll(self, value):
        self.roll = self._update(self.roll, value)
        super().set_roll(self.roll)

    def _update(self, old, new, max_delta=0.3):
        if abs(old - new) <= max_delta:
            res = new
        else:
            res = 0.0
        return res


class DroneEventHandler:
    def __init__(self,
                 flight: Flight,
                 flight_config: FlightConfig,
                 competition_db: Optional[CompetitionDatabase] = None):
        self.flight = flight
        self.competition_db = competition_db
        self._prev_flight_data = None
        self.flight_data = None
        self.flight_config: FlightConfig = flight_config
        self.log_data = None
        self._last_print_second: int = 1

    def handler(self, event, sender, data):
        drone: TelloDrone = sender

        if event is drone.EVENT_FLIGHT_DATA and self.flight_config.print_flight_data:
            if self._prev_flight_data != str(data):
                self._prev_flight_data = str(data)
            self.flight_data = data
            self.print_data(data)

        elif event is drone.EVENT_LOG_DATA:
            self.log_data = data
            flight_pos = FlightPosition(
                flight=self.flight,
                ts=datetime.utcnow(),
                x=data.mvo.pos_x,
                y=data.mvo.pos_y,
                z=data.mvo.pos_z
            )

            if self.flight_config.db_write_data:
                self.competition_db.insert_flight_position(flight_pos)

            if self.flight_config.print_positional_data:
                self.print_data(data.mvo.pos_x, data.mvo.pos_y, data.mvo.pos_z)

        elif self.flight_config.print_unknown_events:
            self.print_data('unknown event="%s" data=%s' % (event.getname(), str(data)))

    def print_data(self, *args):
        now = datetime.now()
        second: int = now.second
        if self._last_print_second == second:
            return
        self._last_print_second = second

        print(datetime.now(), ' ', *args, end=' ')
        if self.flight and self.flight_config.print_pilot_data:
            print(self.flight.pilot)
        else:
            print()
