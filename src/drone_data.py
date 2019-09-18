from drone import TelloDrone
from tellopy._internal.event import Event
from tellopy._internal.protocol import FlightData

class DroneData:
  _prev_flight_data = None
  flight_data = None
  log_data = None

  def handler(self, event: Event, sender: TelloDrone, data: FlightData):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        if self._prev_flight_data != str(data):
            print(data)
            self._prev_flight_data = str(data)
        self.flight_data = data
    elif event is drone.EVENT_LOG_DATA:
        self.log_data = data
    else:
        print('event="%s" data=%s' % (event.getname(), str(data)))
