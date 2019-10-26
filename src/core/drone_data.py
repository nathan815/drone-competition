from datetime import datetime

from core.database import CompetitionDatabase
from .drone import TelloDrone
from .flight import Flight, FlightPosition

PRINT_PILOT = True
PRINT_FLIGHT_DATA = False
PRINT_LOG_DATA = True
PRINT_UNKNOWN_EVENTS = False


class DroneData:
    def __init__(self, flight: Flight, competition_db: CompetitionDatabase):
        self.flight = flight
        self.competition_db = competition_db
        self._prev_flight_data = None
        self.flight_data = None
        self.log_data = None
        self._last_print_second: int = 1

    def event_handler(self, event, sender, data):
        drone: TelloDrone = sender

        if event is drone.EVENT_FLIGHT_DATA and PRINT_FLIGHT_DATA:
            if self._prev_flight_data != str(data):
                self._prev_flight_data = str(data)
            self.flight_data = data
            self.print_data(data)

        elif event is drone.EVENT_LOG_DATA:
            self.log_data = data
            flight_pos = FlightPosition(
                flight=self.flight,
                ts=datetime.now(),
                x=data.mvo.pos_x,
                y=data.mvo.pos_y,
                z=data.mvo.pos_z
            )
            self.competition_db.insert_flight_position(flight_pos)
            if PRINT_LOG_DATA:
                self.print_data(data.mvo.pos_x, data.mvo.pos_y, data.mvo.pos_z)

        elif PRINT_UNKNOWN_EVENTS:
            self.print_data('event="%s" data=%s' % (event.getname(), str(data)))

    def print_data(self, *args):
        now = datetime.datetime.now()
        second: int = now.second
        if self._last_print_second == second:
            return
        self._last_print_second = second

        print(datetime.datetime.now(), " ", *args, end="  ")
        print(self.flight.pilot if self.flight and PRINT_PILOT else '')
