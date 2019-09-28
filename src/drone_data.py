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

        if event is drone.EVENT_FLIGHT_DATA:
            if self._prev_flight_data != str(data):
                self._prev_flight_data = str(data)
            self.flight_data = data
            text_to_print = data
            do_print = do_print and PRINT_FLIGHT_DATA

        elif event is drone.EVENT_LOG_DATA:
            self.log_data = data
            text_to_print = data
            do_print = do_print and PRINT_LOG_DATA

        else:
            text_to_print = 'event="%s" data=%s' % (event.getname(), str(data))
            do_print = do_print and PRINT_UNKNOWN_EVENTS

        if do_print:
            pilot_data = str(self.pilot) if self.pilot else ""
            print(datetime.datetime.now(), " ", pilot_data, end="  ")
            print(text_to_print)
