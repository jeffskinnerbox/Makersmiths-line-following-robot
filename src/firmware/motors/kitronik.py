import time

import board
import busio

from motors.base import MotorDriver


class KitronikMotorDriver(MotorDriver):
    """Kitronik Robotics Board (5329) motor driver via PCA9685 over I2C.

    I2C: GP8 (SDA), GP9 (SCL), address 0x6C.
    Channel map: M1_FWD=8, M1_REV=9 (left wheel); M2_FWD=10, M2_REV=11 (right wheel).
    Direct PCA9685 register writes — no external library required.
    """

    _ADDR = 0x6C
    _M1_FWD = 8
    _M1_REV = 9
    _M2_FWD = 10
    _M2_REV = 11
    _DEADBAND = 0.05

    def __init__(self):
        self._i2c = busio.I2C(board.GP9, board.GP8)
        while not self._i2c.try_lock():
            pass
        self._wake()

    def _wake(self):
        """Wake PCA9685: enable auto-increment, clear SLEEP bit."""
        self._i2c.writeto(self._ADDR, bytes([0x00, 0x20]))
        time.sleep(0.005)

    def _set_channel(self, channel, counts):
        """Set PCA9685 channel duty cycle. counts: 0–4095."""
        base = 0x06 + 4 * channel
        if counts <= 0:
            data = bytes([base, 0x00, 0x00, 0x00, 0x10])  # FULL OFF
        else:
            counts = min(counts, 4095)
            data = bytes([base, 0x00, 0x00, counts & 0xFF, (counts >> 8) & 0x0F])
        self._i2c.writeto(self._ADDR, data)

    def _speed_to_counts(self, speed):
        """Convert float speed to PCA9685 counts with deadband and clamping."""
        if abs(speed) < self._DEADBAND:
            return 0
        speed = max(-1.0, min(1.0, speed))
        return int(abs(speed) * 4095)

    def set_speeds(self, left, right):
        """Set left and right motor speeds. Range: -1.0 (reverse) to +1.0 (forward)."""
        l_counts = self._speed_to_counts(left)
        r_counts = self._speed_to_counts(right)

        if left >= 0:
            self._set_channel(self._M1_FWD, l_counts)
            self._set_channel(self._M1_REV, 0)
        else:
            self._set_channel(self._M1_FWD, 0)
            self._set_channel(self._M1_REV, l_counts)

        if right >= 0:
            self._set_channel(self._M2_FWD, r_counts)
            self._set_channel(self._M2_REV, 0)
        else:
            self._set_channel(self._M2_FWD, 0)
            self._set_channel(self._M2_REV, r_counts)

    def stop(self):
        """Stop both motors immediately."""
        for ch in (self._M1_FWD, self._M1_REV, self._M2_FWD, self._M2_REV):
            self._set_channel(ch, 0)
