import datetime

from drone import TelloDrone
from pilot import Pilot

PRINT_FLIGHT_DATA = True
PRINT_LOG_DATA = True
PRINT_UNKNOWN_EVENTS = True


class DroneData:
    _prev_flight_data = None
    flight_data = None
    log_data = None
    pilot = None
    last_print_second = 1

    def __init__(self, pilot: Pilot):
        self.pilot = pilot

    def event_handler(self, event, sender: TelloDrone, data):
        drone = sender

        # only print once a second
        do_print = self.last_print_second != datetime.time.second
        self.last_print_second = datetime.time.second

        if not do_print:
            return

        if event is drone.EVENT_FLIGHT_DATA and PRINT_FLIGHT_DATA:
            if self._prev_flight_data != str(data):
                self._prev_flight_data = str(data)
            self.flight_data = data
            print_data(data)

        elif event is drone.EVENT_LOG_DATA and PRINT_LOG_DATA:
            self.log_data = data
            print_data('x=',data.mvo.pos_x, 'y=', data.mvo.pos_y, 'z=', data.mvo.pos_z)

        elif PRINT_UNKNOWN_EVENTS:
            print_data('event="%s" data=%s' % (event.getname(), str(data)))


def print_data(*args):
    print(datetime.datetime.now(), " ", *args, end="  ")
