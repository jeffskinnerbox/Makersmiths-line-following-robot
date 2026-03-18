import board
import digitalio

from sensors.base import LineSensor


class IRPairSensor(LineSensor):
    """Two-sensor IR emitter/phototransistor pair for DS3–DS5.

    Left sensor: GP2, Right sensor: GP3.
    read_raw() returns [0, 1] where 0 = on-line (dark line detected), 1 = off-line.
    """

    def __init__(self):
        self._left = digitalio.DigitalInOut(board.GP2)
        self._left.direction = digitalio.Direction.INPUT
        self._right = digitalio.DigitalInOut(board.GP3)
        self._right.direction = digitalio.Direction.INPUT

    @property
    def num_sensors(self):
        return 2

    def calibrate(self):
        pass  # no-op: digital sensors use hardware threshold

    def read_raw(self):
        """Return [left_val, right_val] where 0 = on-line, 1 = off-line."""
        return [int(self._left.value), int(self._right.value)]

    def read_position(self):
        """Return line position: -1.0 (left), +1.0 (right), 0.0 (both/neither)."""
        raw = self.read_raw()
        left_on = raw[0] == 0
        right_on = raw[1] == 0
        if left_on and not right_on:
            return -1.0
        if right_on and not left_on:
            return 1.0
        return 0.0

    def line_detected(self):
        """Return True if either sensor detects the line."""
        raw = self.read_raw()
        return raw[0] == 0 or raw[1] == 0
