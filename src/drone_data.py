from drone import TelloDrone


class DroneData:
    _prev_flight_data = None
    flight_data = None
    log_data = None

    def handler(self, event, sender: TelloDrone, data):
        drone = sender
        if event is drone.EVENT_FLIGHT_DATA:
            if self._prev_flight_data != str(data):
                print(data)
                self._prev_flight_data = str(data)
            self.flight_data = data
        elif event is drone.EVENT_LOG:
            self.log_data = data
        else:
            print('event="%s" data=%s' % (event.getname(), str(data)))