"""QTRX-MD-08RC 8-channel reflectance sensor array for DS6+.

RC timing-based reads via GP0-GP7. LED control via GP10 (CTRL pin).
Calibration stores per-sensor min/max timing to normalize readings.

RC timing sequence per sensor:
  1. Drive pin HIGH (charge capacitor, ~10 µs)
  2. Set pin to input (high-impedance)
  3. Measure discharge time — shorter = more reflective (white), longer = less (black)
"""

import time
import board
import digitalio

from sensors.base import LineSensor

_NUM_SENSORS = 8
_CHARGE_TIME = 0.000010    # 10 µs capacitor charge
_TIMEOUT_NS = 1_000_000    # 1 ms timeout per sensor (nanoseconds)

_SENSOR_PINS = [
    board.GP0, board.GP1, board.GP2, board.GP3,
    board.GP4, board.GP5, board.GP6, board.GP7,
]
_CTRL_PIN = board.GP10


class QTRXArray(LineSensor):
    """8-channel QTRX-MD-08RC reflectance sensor array.

    Sensors on GP0-GP7, LED control (CTRL) on GP10.
    RC timing: longer discharge time -> darker surface (on-line).

    read_raw() returns calibration-normalized floats in [0.0, 1.0]:
        1.0 = fully on-line (black), 0.0 = fully off-line (white).
    """

    def __init__(self):
        self._ctrl = digitalio.DigitalInOut(_CTRL_PIN)
        self._ctrl.direction = digitalio.Direction.OUTPUT
        self._ctrl.value = False  # LEDs off until reading

        self._pins = []
        for p in _SENSOR_PINS:
            pin = digitalio.DigitalInOut(p)
            self._pins.append(pin)

        # Per-sensor calibration bounds (nanoseconds)
        self._cal_min = [0] * _NUM_SENSORS           # white surface (fast discharge)
        self._cal_max = [_TIMEOUT_NS] * _NUM_SENSORS  # black surface (slow discharge)

        self._last_position = 0.0
        self._line_lost = False

    # ------------------------------------------------------------------
    # LineSensor interface
    # ------------------------------------------------------------------

    @property
    def num_sensors(self):
        return _NUM_SENSORS

    def calibrate(self, samples=50):
        """Record min/max discharge time per sensor over `samples` reads.

        Move the robot over a black line on white background while calling this.
        Updates internal calibration tables used by read_raw().
        """
        mins = [_TIMEOUT_NS] * _NUM_SENSORS
        maxs = [0] * _NUM_SENSORS

        for _ in range(samples):
            timings = self._read_raw_timings()
            for i, t in enumerate(timings):
                if t < mins[i]:
                    mins[i] = t
                if t > maxs[i]:
                    maxs[i] = t

        self._cal_min = mins
        self._cal_max = maxs

    def read_raw(self):
        """Return 8 calibration-normalized floats in [0.0, 1.0].

        1.0 = on-line (black / slow discharge), 0.0 = off-line (white / fast discharge).
        Values clamped to [0.0, 1.0]; zero calibration span returns 0.0.
        """
        timings = self._read_raw_timings()
        result = []
        for i, t in enumerate(timings):
            span = self._cal_max[i] - self._cal_min[i]
            if span == 0:
                result.append(0.0)
            else:
                v = (t - self._cal_min[i]) / span
                result.append(max(0.0, min(1.0, v)))
        return result

    def read_position(self):
        """Weighted-average line position in [-1.0, +1.0].

        -1.0 = line under sensor 1 (leftmost), +1.0 = sensor 8 (rightmost).
        Returns last known position if line is lost (line-lost memory).
        """
        values = self.read_raw()
        total = sum(values)

        if total < 0.1:
            self._line_lost = True
            return self._last_position

        # Sensor positions evenly spaced: -1.0, -0.714, ..., +0.714, +1.0
        positions = [-1.0 + i * (2.0 / (_NUM_SENSORS - 1)) for i in range(_NUM_SENSORS)]
        position = sum(v * p for v, p in zip(values, positions)) / total

        self._line_lost = False
        self._last_position = position
        return position

    def line_detected(self):
        """Return True if at least one sensor is on the line."""
        return sum(self.read_raw()) >= 0.1

    @property
    def line_lost(self):
        """True when read_position() last returned a remembered position."""
        return self._line_lost

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_raw_timings(self):
        """Measure RC discharge time (ns) for all 8 sensors.

        Enables LED emitters, reads all sensors, then disables LEDs.
        Returns list of 8 ints (nanoseconds). Capped at _TIMEOUT_NS.
        """
        self._ctrl.value = True
        timings = [self._read_one_timing(i) for i in range(_NUM_SENSORS)]
        self._ctrl.value = False
        return timings

    def _read_one_timing(self, idx):
        """RC timing read for one sensor. Returns nanoseconds elapsed until discharge."""
        pin = self._pins[idx]
        pin.direction = digitalio.Direction.OUTPUT
        pin.value = True
        time.sleep(_CHARGE_TIME)
        pin.direction = digitalio.Direction.INPUT
        start = time.monotonic_ns()
        while pin.value:
            if time.monotonic_ns() - start > _TIMEOUT_NS:
                return _TIMEOUT_NS
        return time.monotonic_ns() - start
