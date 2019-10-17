import datetime
from .drone import TelloDrone
from .pilot import Pilot

PRINT_PILOT = True
PRINT_FLIGHT_DATA = False
PRINT_LOG_DATA = True
PRINT_UNKNOWN_EVENTS = False


class DroneData:
    _prev_flight_data = None
    flight_data = None
    log_data = None
    pilot: Pilot = None
    _last_print_second: int = 1

    def __init__(self, pilot: Pilot):
        self.pilot = pilot

    def event_handler(self, event, sender, data):
        drone: TelloDrone = sender

        if event is drone.EVENT_FLIGHT_DATA and PRINT_FLIGHT_DATA:
            if self._prev_flight_data != str(data):
                self._prev_flight_data = str(data)
            self.flight_data = data
            self.print_data(data)

        elif event is drone.EVENT_LOG_DATA and PRINT_LOG_DATA:
            self.log_data = data
            # print("EVENT!!!", event, data)
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
        print(self.pilot if self.pilot and PRINT_PILOT else '')


class DroneDataHandler:
    _drone_data: DroneData = None

    def __init__(self, drone_data):
        self._drone_data = drone_data

    def print(self):
        pass


class PrintDroneDataHandler(DroneDataHandler):
    def print(self, event, sender: TelloDrone, data):
        pass
