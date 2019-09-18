from tellopy import Tello


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
